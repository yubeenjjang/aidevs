"""부산과 서울 지역의 관광지 정보를 제공하는 교육용 stdio MCP Server"""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "tour",
    instructions="부산과 서울의 관광지 정보를 제공합니다.",
)


@mcp.tool()
def get_current_tour(city: Literal["부산", "서울"]) -> dict:
    """도시의 현재 관광 정보를 조회합니다."""
    tour = {
        "부산": {
            "place": "해운대 해수욕장",
            "category": "바다",
            "description": "부산의 대표적인 해변 관광지입니다.",
            "recommendation": "해변 산책과 야경 감상을 추천합니다."
        },
        "서울": {
            "place": "경복궁",
            "category": "역사",
            "description": "서울의 대표적인 궁궐 관광지입니다.",
            "recommendation": "한복 체험과 궁궐 관람을 추천합니다."
        },
    }

    return {
        "city": city,
        **tour[city],
        "source": "lab-tour-service",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
