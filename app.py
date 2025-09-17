import os
import re
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


def _load_api_key_from_config_js():
    """Если переменная окружения OPENAI_API_KEY не задана, попытаться
    распарсить локальный `config.js` и установить её в процесс.
    """
    if os.environ.get("OPENAI_API_KEY"):
        return
    cfg_path = os.path.join(os.path.dirname(__file__), "config.js")
    if not os.path.exists(cfg_path):
        return
    try:
        content = open(cfg_path, "r", encoding="utf-8").read()
        # простой regexp: ищем OPENAI_API_KEY: "..."
        m = re.search(r'OPENAI_API_KEY\s*:\s*"([^"]+)"', content)
        if m:
            os.environ["OPENAI_API_KEY"] = m.group(1)
    except Exception:
        # ничего не делаем при ошибке чтения/парсинга
        pass


# Попытка загрузить ключ сразу при импорте
_load_api_key_from_config_js()


def generate_response(prompt: str) -> str:
    """Generate a reply to `prompt`.

    If environment variable OPENAI_API_KEY is set, try to use OpenAI's API.
    Otherwise return a simple deterministic fallback response.
    """
    # Получаем OpenAI API ключ из переменной окружения
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            # lazy import so app can run without openai installed
            import openai
            openai.api_key = api_key
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI error] {e}"

    # Fallback toy LLM: simple echo + canned help
    prompt = prompt.strip()
    if not prompt:
        return "Сформулируйте, пожалуйста, вопрос."
    if "привет" in prompt.lower() or "hello" in prompt.lower():
        return "Привет! Я простая LLM-демонстрация. Задайте вопрос." 
    if "как" in prompt.lower() and "сделать" in prompt.lower():
        return "Попробуйте разбить задачу на шаги и выполнять по одному."
    # default: short synthetic answer
    return "Это демонстрационный ответ (fallback). Задайте более конкретный вопрос или установите OPENAI_API_KEY для реальной LLM."


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    reply = generate_response(prompt)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
