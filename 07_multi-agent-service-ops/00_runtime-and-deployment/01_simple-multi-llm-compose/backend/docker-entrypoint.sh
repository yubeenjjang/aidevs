#!/bin/sh
set -eu

python /app/init_schema.py
exec uvicorn app:app --host 0.0.0.0 --port 8000
