"""07~08 예제가 공유하는 최소 Ollama RAG 함수입니다."""

import os

import httpx

from _pgvector_store import OLLAMA_BASE_URL, similarity_search


COLLECTION = "baby_rag"
CHAT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "300"))
OLLAMA_MAX_TOKENS = int(os.getenv("OLLAMA_MAX_TOKENS", "96"))


def answer_question(question: str) -> dict:
    results = similarity_search(question, collection=COLLECTION, top_k=3)
    if not results:
        return {"answer": "관련 문서를 찾지 못했습니다.", "sources": []}

    context = "\n".join(
        f"[{item['source']}] {item['content']}" for item in results
    )
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            # CPU 환경에서는 최초 모델 로딩에 2분 이상 걸릴 수 있습니다.
            "keep_alive": "10m",
            # RAG 예제는 긴 생성보다 근거 있는 짧은 답변을 확인하는 데 초점을 둡니다.
            "options": {"num_predict": OLLAMA_MAX_TOKENS},
            "messages": [
                {
                    "role": "system",
                    "content": "Context만 사용해 한국어로 두 문장 이내로 답하고 출처를 표시하세요.",
                },
                {"role": "user", "content": f"질문: {question}\n\nContext:\n{context}"},
            ],
        },
        timeout=OLLAMA_TIMEOUT_SECONDS,
    )
    #해당 응답에 문제 있으면 폭탄, 없으면 괜찬
    response.raise_for_status()
    return {
        "answer": response.json()["message"]["content"],
        "sources": sorted({item["source"] for item in results}),
    }
