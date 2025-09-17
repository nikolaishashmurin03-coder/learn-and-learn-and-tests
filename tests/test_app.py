import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import generate_response


def test_empty_prompt():
    assert generate_response("") == "Сформулируйте, пожалуйста, вопрос."


def test_fallback_answer():
    resp = generate_response("What is the meaning of life?")
    assert isinstance(resp, str) and resp
