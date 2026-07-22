# chat_service.py
# 사용자가 입력한 질문을 Gemini AI에 보내고, 답변을 받아 반환하는 서비스 파일

from app.schemas.chat_schema import ChatRequest, ChatResponse
import os

from google import genai


def call_gemini(chat_request: ChatRequest) -> ChatResponse:
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=chat_request.prompt,
    )

    return ChatResponse(answer=response.text)
