# 게시 날짜가 있는 FastAPI 게시판 프로젝트 계획서

## 1. 프로젝트 개요

`01_http-methods.py`의 코드 형태를 그대로 참고해 간단한 게시판 API를 만든다.

기존 메모 예제의 `Memo`를 `Post`로 변경하고, 제목과 내용 외에 게시 날짜(`published_date`) 필드만 추가한다. 코드는 학습 예제와 동일하게 하나의 Python 파일에 작성하고, Python `dict`를 임시 저장소로 사용한다.

## 2. 구현 목표

- `GET`으로 게시글 목록 조회
- `POST`로 게시글 생성
- `PUT`으로 게시글 수정
- `DELETE`로 게시글 삭제
- 게시글마다 게시 날짜 저장
- Pydantic으로 제목, 내용, 게시 날짜 검증
- 존재하지 않는 게시글에 대한 오류 처리

## 3. 프로젝트 구조

```text
06_board/
├── PROJECT_PLAN.md
├── README.md
└── board.py
```

모든 구현 코드는 `board.py` 한 파일에 작성한다.

## 4. 게시글 데이터 구조

게시글은 다음 네 가지 값을 가진다.

| 필드 | 타입 | 설명 | 조건 |
| --- | --- | --- | --- |
| `id` | `int` | 게시글 번호 | 서버에서 자동 생성 |
| `title` | `str` | 게시글 제목 | 빈 문자열 불가 |
| `content` | `str` | 게시글 내용 | 빈 문자열 불가 |
| `published_date` | `date` | 게시 날짜 | `YYYY-MM-DD` 형식 |

게시글 예시:

```json
{
  "id": 1,
  "title": "FastAPI 시작",
  "content": "Swagger UI에서 API를 확인했습니다.",
  "published_date": "2026-07-15"
}
```

## 5. 요청 모델

### `PostCreate`

게시글 생성 시 제목, 내용, 게시 날짜를 받는다.

```python
class PostCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    published_date: date
```

### `PostUpdate`

`01_http-methods.py`의 `MemoUpdate`처럼 수정할 게시글 번호와 변경할 전체 내용을 받는다.

```python
class PostUpdate(BaseModel):
    id: int = Field(min=1)
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    published_date: date
```

## 6. 메모리 저장소

참고 파일과 동일하게 Python `dict`를 사용한다.

```python
posts = {
    1: {
        "id": 1,
        "title": "FastAPI 시작",
        "content": "Swagger UI에서 API를 확인했습니다.",
        "published_date": date(2026, 7, 15),
    }
}

next_post_id = 2
```

서버를 다시 시작하면 저장한 게시글은 초기 상태로 돌아간다.

## 7. API 설계

`01_http-methods.py`의 URL 구조와 Method 구성을 게시글 이름으로 변경한다.

| Method | 경로 | 기능 | 성공 상태 코드 |
| --- | --- | --- | --- |
| `GET` | `/posts/list` | 전체 게시글 목록 조회 | `200` |
| `POST` | `/posts/create` | 새 게시글 생성 | `201` |
| `PUT` | `/posts` | 기존 게시글 전체 수정 | `200` |
| `DELETE` | `/posts/{post_id}` | 기존 게시글 삭제 | `200` |

## 8. API 동작 계획

### 전체 게시글 목록 조회

```python
@app.get("/posts/list")
```

- `posts.values()`를 리스트로 변환한다.
- 저장된 전체 게시글을 `data`에 담아 반환한다.
- 게시 날짜에 따른 필터링이나 정렬은 적용하지 않는다.

### 게시글 생성

```python
@app.post("/posts/create", status_code=201)
```

- `PostCreate`로 제목, 내용, 게시 날짜를 검증한다.
- `next_post_id`를 새 게시글 번호로 사용한다.
- 새 게시글을 `posts`에 저장한다.
- 저장 후 `next_post_id`를 1 증가시킨다.

### 게시글 수정

```python
@app.put("/posts")
```

- `PostUpdate`에 포함된 `id`로 수정할 게시글을 찾는다.
- 게시글이 없으면 `404` 오류를 반환한다.
- 제목, 내용, 게시 날짜를 요청 값으로 모두 교체한다.

### 게시글 삭제

```python
@app.delete("/posts/{post_id}")
```

- 게시글 번호가 `posts`에 있는지 확인한다.
- 게시글이 없으면 `404` 오류를 반환한다.
- `pop()`으로 게시글을 삭제하고 삭제된 데이터를 반환한다.

## 9. 응답 형식

목록 조회:

```json
{
  "data": []
}
```

생성:

```json
{
  "message": "post created",
  "data": {}
}
```

수정:

```json
{
  "message": "post updated",
  "data": {}
}
```

삭제:

```json
{
  "message": "post deleted",
  "data": {}
}
```

## 10. 오류 처리

| 상황 | 상태 코드 | 내용 |
| --- | --- | --- |
| 수정할 게시글이 없음 | `404` | `Post not found` |
| 삭제할 게시글이 없음 | `404` | `Post not found` |
| 제목 또는 내용이 비어 있음 | `422` | Pydantic 검증 오류 |
| 게시 날짜 형식이 잘못됨 | `422` | Pydantic 검증 오류 |
| 수정 요청의 `id`가 1보다 작음 | `422` | Pydantic 검증 오류 |

## 11. 구현 순서

1. `date`, `FastAPI`, `HTTPException`, `BaseModel`, `Field`를 가져온다.
2. FastAPI 앱 객체를 생성한다.
3. `PostCreate`와 `PostUpdate` 모델을 작성한다.
4. 샘플 데이터가 있는 `posts`와 `next_post_id`를 작성한다.
5. 전체 목록 조회 API를 작성한다.
6. 게시글 생성 API를 작성한다.
7. 게시글 수정 API를 작성한다.
8. 게시글 삭제 API를 작성한다.
9. 각 부분에 `01_http-methods.py`와 같은 학습용 한글 주석을 작성한다.
10. Swagger UI에서 네 개의 API를 테스트한다.

## 12. 테스트 항목

- 전체 게시글 목록에 `published_date`가 표시된다.
- 제목, 내용, 게시 날짜를 전달해 게시글을 생성할 수 있다.
- 생성한 게시글에 자동으로 새로운 `id`가 부여된다.
- 게시글의 제목, 내용, 게시 날짜를 수정할 수 있다.
- 게시글을 삭제할 수 있다.
- 존재하지 않는 게시글을 수정하거나 삭제하면 `404`가 반환된다.
- 제목이나 내용이 비어 있으면 `422`가 반환된다.
- 게시 날짜가 `YYYY-MM-DD` 형식이 아니면 `422`가 반환된다.

## 13. 실행 방법

```powershell
cd C:\aidevs\02_supabase-ai-backend\01_fastapi-backend\06_board
python -m uvicorn board:app --reload
```

Swagger UI 주소:

```text
http://127.0.0.1:8000/docs
```

## 14. 완료 기준

- `board.py` 한 파일로 구현되어 있다.
- 참고 파일과 동일하게 네 가지 HTTP Method를 사용한다.
- 게시글 생성과 수정 모델에 `published_date`가 포함되어 있다.
- 게시 날짜는 별도 조건 없이 입력, 저장, 조회, 수정된다.
- 목록, 생성, 수정, 삭제 API가 Swagger UI에서 정상 작동한다.
- 참고 파일과 비슷한 형식의 한글 주석이 포함되어 있다.
