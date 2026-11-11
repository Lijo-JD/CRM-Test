@echo off
setlocal
set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

if not exist .venv (
  echo Environment not generated yet. Run generate.bat first.
  exit /b 1
)

call .venv\Scripts\activate
set PORT=8001
start "CRM Backend" cmd /k "cd /d \"%ROOT_DIR%\backend\" && python -m uvicorn app.main:app --host 0.0.0.0 --port %PORT%"
cd /d "%ROOT_DIR%\frontend"
call npm run dev
