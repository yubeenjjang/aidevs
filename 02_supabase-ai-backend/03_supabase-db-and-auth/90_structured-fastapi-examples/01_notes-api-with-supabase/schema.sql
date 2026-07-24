-- 01_notes-api-with-supabase 예제에서 사용하는 테이블입니다.
--
-- 이 예제의 목표:
-- 1. FastAPI 구조를 router/schema/service로 나눕니다.
-- 2. service 계층에서 Supabase 테이블을 CRUD합니다.
-- 3. 인증/RLS 없이 가장 단순한 DB 연결 흐름부터 확인합니다.

create table if not exists ex90_notes (
  -- id는 각 노트를 구분하는 고유값입니다.
  -- gen_random_uuid()는 Supabase/PostgreSQL이 자동으로 uuid를 만들어 줍니다.
  id uuid primary key default gen_random_uuid(),

  -- title/content는 사용자가 입력하는 필수 텍스트입니다.
  title text not null,
  content text not null,

  -- created_at은 row가 만들어진 시간을 자동 기록합니다.
  created_at timestamp not null default now()
);

-- API 실습에 사용할 샘플 메모 10개를 추가합니다.
-- id와 created_at은 테이블에 정의된 기본값으로 자동 생성됩니다.
insert into ex90_notes (title, content)
values
  ('첫 번째 메모', 'Supabase 프로젝트 설정 방법을 정리합니다.'),
  ('FastAPI 학습', '라우터, 스키마, 서비스 계층의 역할을 복습합니다.'),
  ('데이터베이스 연결', '환경 변수를 이용해 Supabase 연결 정보를 관리합니다.'),
  ('CRUD 구현', '메모 생성, 조회, 수정, 삭제 기능을 구현합니다.'),
  ('API 테스트', 'Swagger UI에서 각 API 엔드포인트를 테스트합니다.'),
  ('오류 처리', '데이터가 없을 때 반환할 오류 응답을 정의합니다.'),
  ('코드 리팩터링', '중복 코드를 제거하고 모듈 구조를 개선합니다.'),
  ('보안 점검', 'API 키가 소스 코드에 노출되지 않았는지 확인합니다.'),
  ('배포 준비', '운영 환경에서 사용할 환경 변수를 점검합니다.'),
  ('프로젝트 완료', '최종 테스트 후 프로젝트를 배포합니다.');
