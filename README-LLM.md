# Минимальный LLM чат (локально)

Этот проект предоставляет минимальный Flask-бэкенд и простую HTML-страницу для общения с очень простой LLM.

Особенности:
- Если у вас есть `OPENAI_API_KEY` в окружении — приложение попытается использовать OpenAI (gpt-3.5-turbo).
- Если `OPENAI_API_KEY` отсутствует, используется простой fallback (toy LLM).

Установка (Windows, PowerShell):

```powershell
cd E:\test\learn-and-learn-and-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Запуск:

```powershell
# (опционально) экспортируйте ключ OpenAI
$env:OPENAI_API_KEY = "sk-..."
python app.py
```

Откройте браузер: `http://localhost:5000` и задавайте вопросы.

Тесты (опционально):

```powershell
.\.venv\Scripts\Activate.ps1
pip install pytest
pytest -q
```

Безопасность: Если вы используете `OPENAI_API_KEY`, не сохраняйте ключ в публичных репозиториях.