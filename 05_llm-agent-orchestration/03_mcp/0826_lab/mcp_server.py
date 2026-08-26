"""stdio로 실행되는 개인 건강 습관 관리 MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "health-habit-tools",
    instructions="개인 건강 습관을 관리해주는 교육용 MCP Server입니다.",
    
)


#오래 앉아 있는 습관
@mcp.tool()
def checking_sitting_habit(sitting_minutes: int) -> dict :
    """연속으로 앉아 있는 시간을 기준으로 생활 습관을 확인합니다."""
    
    normalized  = sitting_minutes
    
    #RAG
    if normalized < 30 :
        status = "좋음"
        message = "현재 앉아 있는 시간은 적절합니다."
    
    elif normalized < 60 :
        status = "주의"
        message = "잠깐 일어나서 걷거나 스트레칭해보세요."
    
    else:
        status = "개선 필요"
        message = "오랜 시간 앉아 있었습니다. 가볍게 몸을 움직여보세요."
    
    return {
        "sitting_minutes" : sitting_minutes,
        "status": status,
        "message": message
    }
    
#카페인 섭취 습관
@mcp.tool()
def check_caffeine_timing(cups: int, last_caffeine_hour: int) -> dict:
    """하루 카페인 섭취량과 마지막 섭취 시간을 기준으로 카페인 습관을 확인합니다."""

    normalized = last_caffeine_hour

    # RAG
    if cups <= 2 and normalized < 15:
        status = "좋음"
        message = "카페인 섭취 습관이 비교적 적절합니다."

    elif normalized >= 18:
        status = "주의"
        message = "늦은 시간의 카페인 섭취는 줄여보는 것이 좋습니다."

    else:
        status = "보통"
        message = "카페인 섭취량과 시간을 조금 조절해보세요."

    return {
        "cups": cups,
        "last_caffeine_hour": last_caffeine_hour,
        "status": status,
        "message": message
    }

#디지털 기기 사용 습관
@mcp.tool()
def check_screen_break_habit(
    screen_minutes: int,
    break_minutes: int
) -> dict:
    """디지털 기기 연속 사용 시간과 휴식 시간을 기준으로 사용 습관을 확인합니다."""

    normalized = screen_minutes

    # RAG
    if normalized <= 30 and break_minutes >= 5:
        status = "좋음"
        message = "적절하게 화면 사용 중 휴식을 취하고 있습니다."

    elif normalized <= 60:
        status = "주의"
        message = "잠시 화면에서 눈을 떼고 휴식을 취해보세요."

    else:
        status = "개선 필요"
        message = "디지털 기기를 오래 사용했습니다. 잠시 눈과 몸을 쉬어주세요."

    return {
        "screen_minutes": screen_minutes,
        "break_minutes": break_minutes,
        "status": status,
        "message": message
    }


if __name__ == "__main__":
    print("MCP server is running on stdio....")
    mcp.run(transport="stdio")
