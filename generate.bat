@echo off
setlocal
set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

where python >nul 2>nul
if errorlevel 1 (
  echo Python 3 is required but not installed.
  exit /b 1
)

where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is required but not installed.
  exit /b 1
)

if not exist .env copy .env.example .env

python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt

cd frontend
call npm install
cd /d "%ROOT_DIR%"

echo Generation complete. Run run.bat to start the app.
