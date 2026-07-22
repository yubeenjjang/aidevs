from fastapi.testclient import TestClient

from app.main import app
from app.routers import chat_router
from app.schemas.chat_schema import ChatResponse


client = TestClient(app)


def test_chat_gemini_returns_service_response(monkeypatch):
    received = {}

    def fake_call_gemini(chat_request):
        received["request"] = chat_request
        return ChatResponse(answer="test response")

    monkeypatch.setattr(chat_router, "call_gemini", fake_call_gemini)

    response = client.post(
        "/chat/gemini",
        json={"use_id": "user-1", "prompt": "hello"},
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "test response"}
    assert received["request"].use_id == "user-1"
    assert received["request"].prompt == "hello"


def test_chat_gemini_rejects_empty_prompt():
    response = client.post(
        "/chat/gemini",
        json={"use_id": "user-1", "prompt": ""},
    )

    assert response.status_code == 422


def test_chat_gemini_rejects_missing_use_id():
    response = client.post(
        "/chat/gemini",
        json={"prompt": "hello"},
    )

    assert response.status_code == 422
