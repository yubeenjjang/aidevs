# LLM API Integration Mini Project

FastAPI에서 Gemini API를 호출하는 채팅 API와 간단한 상품 API를 구현한 미니 프로젝트입니다. 라우터, 스키마, 서비스 계층을 분리하고 pytest로 각 라우터를 검증합니다.

## 주요 기능

- Gemini 단일 질문/응답 API
- 상품 생성, 단건 조회, 전체 조회 API
- Pydantic 기반 요청·응답 검증
- FastAPI 자동 API 문서
- 외부 Gemini 호출을 mock 처리한 라우터 테스트

## 프로젝트 구조

```text
00_mini_project/
├─ app/
│  ├─ core/
│  │  └─ chat_config.py
│  ├─ routers/
│  │  ├─ chat_router.py
│  │  └─ product_router.py
│  ├─ schemas/
│  │  ├─ chat_schema.py
│  │  └─ product_schema.py
│  ├─ services/
│  │  ├─ chat_service.py
│  │  └─ product_service.py
│  └─ main.py
└─ tests/
   ├─ test_chat_router.py
   └─ test_product_router.py
```

## 실행 환경

- Python 3.12 권장
- FastAPI
- Uvicorn
- Google Gen AI SDK
- pytest

공통 의존성과 가상환경은 저장소 루트인 `02_supabase-ai-backend`에서 관리합니다.

## 설치

PowerShell에서 저장소 루트로 이동한 후 다음 명령을 실행합니다.

```powershell
cd C:\aidevs\02_supabase-ai-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

이미 `.venv`가 준비되어 있다면 가상환경 활성화와 패키지 설치만 진행하면 됩니다.

## 환경변수 설정

저장소 루트의 `.env.example`을 `.env`로 복사합니다.

```powershell
cd C:\aidevs\02_supabase-ai-backend
Copy-Item .env.example .env
```

`.env`에서 Gemini 설정을 입력합니다.

```dotenv
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

`GEMINI_API_KEY`는 실제 키로 변경해야 합니다. `.env`는 Git에 커밋하지 않습니다.

## 서버 실행

```powershell
cd C:\aidevs\02_supabase-ai-backend\02_llm-api-integration\00_mini_project
..\..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

서버 실행 후 다음 주소를 사용할 수 있습니다.

- API 기본 주소: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API 목록

| Method | Endpoint | 설명 |
|---|---|---|
| `POST` | `/chat/gemini` | Gemini에 질문하고 답변을 반환합니다. |
| `POST` | `/product/create` | 상품 정보를 전달하고 생성 결과를 반환합니다. |
| `GET` | `/product/get/{product_id}` | ID에 해당하는 샘플 상품을 반환합니다. |
| `GET` | `/product/getall` | 전체 샘플 상품 목록을 반환합니다. |

현재 상품 서비스는 학습용 구현으로, 실제 데이터베이스에 저장하지 않습니다.

## API 호출 예시

### Gemini 채팅

요청 스키마의 사용자 ID 필드명은 현재 코드 기준으로 `use_id`입니다.

```powershell
$body = @{
    use_id = "user-01"
    prompt = "FastAPI를 한 문장으로 설명해 줘"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/chat/gemini" `
    -ContentType "application/json" `
    -Body $body
```

응답 예시:

```json
{
  "answer": "FastAPI는 Python 타입 힌트를 활용해 빠르게 API를 만들 수 있는 웹 프레임워크입니다."
}
```

### 상품 생성

```powershell
$body = @{
    id = "product-1"
    name = "keyboard"
    price = 50000
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/product/create" `
    -ContentType "application/json" `
    -Body $body
```

### 상품 단건 조회

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/get/product-1"
```

### 상품 전체 조회

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/product/getall"
```

## 테스트

프로젝트 폴더에서 다음 명령을 실행합니다.

```powershell
cd C:\aidevs\02_supabase-ai-backend\02_llm-api-integration\00_mini_project
..\..\.venv\Scripts\python.exe -m pytest tests -q
```

테스트는 라우터별 파일로 분리되어 있습니다.

- `test_chat_router.py`: 정상 채팅 요청과 요청 데이터 검증
- `test_product_router.py`: 상품 생성, 단건 조회, 전체 조회와 요청 데이터 검증

채팅 테스트에서는 Gemini 서비스를 mock 처리하므로 API 키가 없어도 실행할 수 있으며 실제 API 비용도 발생하지 않습니다.

## 참고 사항

- 실제 Gemini API 호출에는 인터넷 연결과 유효한 `GEMINI_API_KEY`가 필요합니다.
- 빈 `use_id` 또는 `prompt`, 필수 상품 필드 누락 시 FastAPI가 `422 Unprocessable Entity`를 반환합니다.
- 운영 환경에서는 API 키 관리, 예외 처리, 로깅, 비동기 호출, 데이터베이스 저장 기능을 추가해야 합니다.
