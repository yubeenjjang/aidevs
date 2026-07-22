"""
uvicorn 00_http:app --reload

python -m uvicorn main:app --reload

"""

from fastapi import FastAPI
from dataclasses import dataclass

app = FastAPI(
    title="First FastAPI",
    description="FastAPI 서버가 어떻게 시작되는지 확인하는 첫 예제입니다.",
    version="1.0.0",
)
# Model
# 1. Memo


# 데이터를 저장하는 클래스를 간단하게 만들기 위한 데코레이터
@dataclass
class Memo:
    id: int
    title: str
    content: str


# Mock Data
memos = []

memos.extend(
    [
        Memo(id=100, title="제목", content="하이루"),
        Memo(id=300, title="제목", content="하이루"),
        Memo(id=200, title="제목", content="하이루"),
    ]
)


@app.get("/memo/get/{memo_id}")
def read_memo(memo_id: int) -> Memo:
    """read_memo"""
    return Memo(
        id=100,
        title="제목",
        content="하이루",
    )


@app.get("/memo/getall")
def readall_memo() -> list[Memo]:
    """readall_memo"""
    return memos


@app.post("/memo/create")
def create_memo(memo: Memo):
    """create_memo"""
    return


@app.put("/modify")
def modify_memo():
    """modify_memo"""
    return


@app.delete("/remove")
def remove_memo():
    """remove_memo"""
    return
