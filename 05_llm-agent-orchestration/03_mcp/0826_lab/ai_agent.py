#06_mcp_call.py

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI

from _stdio_client import connect_to_health_server


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

INSTRUCTIONS = (
    "당신은 건강 습관 관리 AI Agent입니다. "
    "사용자의 생활 습관과 관련된 요청을 분석하고 필요한 Tool을 사용하세요. "
    "오래 앉아 있는 습관은 check_sitting_habit Tool을 사용하세요. "
    "카페인 섭취 습관은 check_caffeine_timing Tool을 사용하세요. "
    "디지털 기기 사용 습관은 check_screen_break_habit Tool을 사용하세요. "
    "사용자가 여러 습관을 함께 이야기하면 필요한 Tool을 모두 호출하세요. "
    "Tool을 호출하기 전에 최종 답변을 작성하지 마세요. "
)


# MCP Tool을 OpenAI에서 사용할 수 있는 Tool 형식으로 변환
def to_openai_tool(tool) -> dict[str, Any]:
    """MCP Tool Schema를 OpenAI Responses API의 Function Tool로 변환합니다."""
    raw = tool.model_dump(by_alias=True)
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": raw["inputSchema"],
        "strict": False,
    }

# MCP Tool 실행 결과에서 text만 추출
def text_result(result) -> str:
    return "\n".join(
        content.text for content in result.content if hasattr(content, "text")
    )

#사용자 질문 받으면 agent 실행
async def answer(question: str) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다.")

    trace: list[dict[str, Any]] = []

    async with AsyncOpenAI() as client, connect_to_health_server() as session:
        # MCP Server가 가지고 있는 Tool 목록 가져오기
        discovered = (await session.list_tools()).tools
        
        # 사용 가능한 Tool 이름
        available = {tool.name for tool in discovered}
        
        # MCP Tool → OpenAI Tool 형식으로 변환
        openai_tools = [to_openai_tool(tool) for tool in discovered]
        
        # 1차 GPT 호출
        # 어떤 Tool이 필요한지 판단
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            input=question,
            tools=openai_tools,
            #여러 건강 습관을 물어보면 여러 tool의 결과를 한꺼번에 보여줌
            parallel_tool_calls=True,
        )
        # GPT가 선택한 Tool 가져오기
        tool_calls = [item for item in response.output if item.type == "function_call"]
        # Tool이 필요하지 않은 질문이면 그대로 답변
        if not tool_calls:
            return {
                "question": question,
                "model": OPENAI_MODEL,
                "discovered_tools": sorted(available),
                "llm_calls": 1,
                "trace": trace,
                "answer": response.output_text,
            }

        tool_outputs = []
         # MCP Tool 실행
        for call in tool_calls:
            if call.name not in available:
                raise ValueError(f"MCP Server가 제공하지 않는 Tool입니다: {call.name}")
            arguments = json.loads(call.arguments)
            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments는 JSON Object여야 합니다.")

            result = await session.call_tool(call.name, arguments)
            result_text = text_result(result)
            
        
            # 어떤 Tool을 사용했는지 기록
            trace.append({
                "tool": call.name,
                "arguments": arguments,
                "is_error": bool(result.isError),
                "result": result_text,
            })
            
            # Tool 결과를 다시 GPT에게 전달
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text,
            })
            
        # 2차 GPT 호출
        # Tool 결과를 이용해서 최종 답변 생성
        final_response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
        )
        return {
            "question": question,
            "model": OPENAI_MODEL,
            "discovered_tools": sorted(available),
            "llm_calls": 2,
            "trace": trace,
            "answer": final_response.output_text,
        }


async def main() -> None:
    
    # 앉아있는 습관
    # result = await answer(
    #     "오늘 2시간 동안 계속 앉아서 공부했어."
    # )

    # 카페인 습관
    # result = await answer(
    #     "오늘 커피 3잔 마셨고 마지막 커피는 저녁 8시에 마셨어."
    # )

    # 디지털 기기 습관
    result = await answer(
        "노트북을 90분 연속으로 사용하고 5분 쉬었어."
    )

    # 여러 Tool 동시에 호출
    # result = await answer(
    #     "오늘 2시간 동안 계속 앉아 있었고 "
    #     "커피는 3잔 마셨는데 마지막 커피는 저녁 8시에 마셨어. "
    #     "노트북도 90분 연속으로 사용하고 5분 쉬었어."
    # )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
