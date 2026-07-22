r"""learning_notes 삭제 예제입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\03_supabase-db-and-auth\02_supabase-table-and-crud\05_delete_learning_note.py
"""

from supabase_client import get_supabase


def main() -> None:
    """실습용 메모를 만든 뒤 바로 삭제합니다."""

    supabase = get_supabase()

    # created_result = (
    #     supabase.table("learning_notes")
    #     .insert(
    #         {
    #             "title": "Supabase delete practice",
    #             "content": "삭제 실습을 위해 잠시 생성한 메모입니다.",
    #         }
    #     )
    #     .execute()
    # )

    # if not created_result.data:
    #     raise RuntimeError("삭제 실습용 메모를 생성하지 못했습니다.")

    # created = created_result.data[0]
    # note_id = created["id"]
    # print(f"[created for delete]\nid: {note_id}")

    # delete도 update와 마찬가지로 조건이 중요합니다.
    # 조건이 없으면 의도하지 않은 데이터가 삭제될 수 있습니다.
    result = (
        supabase.table("learning_notes").delete().eq("id", "20260721140454").execute()
    )
    print(result.data)


if __name__ == "__main__":
    main()
