@echo off
cd /d "%~dp0.."
echo Starting Cardiac DSS API on http://127.0.0.1:8000
echo API docs: http://127.0.0.1:8000/docs
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
