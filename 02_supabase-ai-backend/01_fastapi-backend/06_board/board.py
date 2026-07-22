"""게시 날짜가 있는 게시판 CRUD API 예제입니다.

이 파일은 GET, POST, PUT, DELETE HTTP Method를 연습하기 위한 학습용 파일입니다.

실행:
    cd C:\aidevs\02_supabase-ai-backend\01_fastapi-backend\06_board
    uvicorn board:app --reload
    # 위 명령에서 오류가 나면 아래처럼 실행합니다.
    python -m uvicorn board:app --reload

브라우저:
    http://127.0.0.1:8000/docs
"""

from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# FastAPI 객체를 만듭니다.
# uvicorn 실행 명령의 마지막 `board:app`은 board.py 파일의 app 변수와 연결됩니다.
app = FastAPI(title="Board HTTP Method Practice")


class PostCreate(BaseModel):
    """POST 요청에서 받을 게시글 생성 데이터입니다."""

    # 제목과 내용은 최소 한 글자 이상이어야 합니다.
    # published_date는 YYYY-MM-DD 형식의 날짜를 받습니다.
    title: str = Field(min_length=1, examples=["오늘 배운 내용"])
    content: str = Field(
        min_length=1,
        examples=["GET과 POST의 차이를 배웠습니다."],
    )
    published_date: date = Field(examples=["2026-07-15"])


class PostUpdate(BaseModel):
    """PUT 요청에서 받을 게시글 수정 데이터입니다."""

    # 수정할 게시글의 id와 새 제목, 내용, 게시 날짜를 모두 받습니다.
    id: int = Field(ge=1, examples=[1])
    title: str = Field(min_length=1, examples=["수정된 제목"])
    content: str = Field(min_length=1, examples=["수정된 내용입니다."])
    published_date: date = Field(examples=["2026-07-16"])


# 서버 메모리에만 저장되는 수업용 게시글 저장소입니다.
# 서버를 종료하거나 다시 시작하면 처음 상태로 돌아갑니다.
# 실제 서비스에서는 이 부분을 Supabase 같은 데이터베이스로 교체합니다.
posts: dict[int, dict[str, object]] = {
    1: {
        "id": 1,
        "title": "FastAPI 시작",
        "content": "Swagger UI에서 API를 확인했습니다.",
        "published_date": date(2026, 7, 15),
    }
}

# 다음에 생성할 게시글의 id입니다.
# 현재 1번 게시글이 있으므로 새 게시글은 2번부터 시작합니다.
next_post_id = 2


# @app.get은 GET 요청을 처리하는 API 주소를 만듭니다.
# GET은 서버에 저장된 데이터를 조회할 때 사용합니다.
@app.get("/posts/list")
def list_posts() -> dict[str, list[dict[str, object]]]:
    """전체 게시글 목록을 조회합니다."""

    # dict.values()로 저장된 게시글 값만 꺼낸 후 list로 변환합니다.
    return {"data": list(posts.values())}


# @app.post는 POST 요청을 처리합니다.
# POST는 새로운 데이터를 만들 때 사용합니다.
# status_code=201은 새로운 리소스 생성에 성공했다는 뜻입니다.
@app.post("/posts/create", status_code=201)
def create_post(post: PostCreate) -> dict[str, object]:
    """새 게시글을 생성합니다."""

    # 함수 안에서 바깥쪽 next_post_id 값을 변경하기 위해 global을 사용합니다.
    global next_post_id

    # FastAPI가 요청 JSON을 PostCreate 모델로 먼저 검증합니다.
    new_post = {
        "id": next_post_id,
        "title": post.title,
        "content": post.content,
        "published_date": post.published_date,
    }

    # 새 게시글을 저장하고 다음 생성 요청에 사용할 id를 준비합니다.
    posts[next_post_id] = new_post
    next_post_id += 1

    return {"message": "post created", "data": new_post}


# @app.put은 PUT 요청을 처리합니다.
# PUT은 기존 데이터를 새로운 전체 내용으로 수정할 때 사용합니다.
@app.put("/posts")
def update_post(post: PostUpdate) -> dict[str, object]:
    """기존 게시글을 수정합니다."""

    # 요청한 id의 게시글이 없으면 404 오류를 반환합니다.
    if post.id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    # 기존 id는 유지하고 제목, 내용, 게시 날짜를 요청 값으로 교체합니다.
    posts[post.id] = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "published_date": post.published_date,
    }

    return {"message": "post updated", "data": posts[post.id]}


# @app.delete는 DELETE 요청을 처리합니다.
# DELETE는 기존 데이터를 삭제할 때 사용합니다.
@app.delete("/posts/{post_id}")
def delete_post(post_id: int) -> dict[str, object]:
    """기존 게시글을 삭제합니다."""

    # 존재하지 않는 게시글을 삭제하려고 하면 404 오류를 반환합니다.
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    # pop은 dict에서 값을 꺼내면서 동시에 삭제합니다.
    deleted = posts.pop(post_id)
    return {"message": "post deleted", "data": deleted}
