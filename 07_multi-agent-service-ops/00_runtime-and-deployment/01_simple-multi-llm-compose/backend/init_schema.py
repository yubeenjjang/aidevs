"""Apply the bundled PostgreSQL schema before the API starts."""

import os
from pathlib import Path

import psycopg


def main() -> None:
    database_url = os.environ["DATABASE_URL"]
    schema_sql = Path("/app/init.sql").read_text(encoding="utf-8")

    with psycopg.connect(database_url, autocommit=True) as connection:
        connection.execute(schema_sql)


if __name__ == "__main__":
    main()
