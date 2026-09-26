@echo off
echo =========================================================================
echo   Starting AgriRaksha (SIH 2026) Complete Full-Stack Environment
echo =========================================================================
echo.
echo 1. Launching Backend Server on http://127.0.0.1:8000 ...
start "AgriRaksha Backend" cmd /c "cd /d %~dp0\..\backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo 2. Launching Frontend Dev Server on http://localhost:3000 ...
start "AgriRaksha Frontend" cmd /c "cd /d %~dp0\..\frontend && npm run dev -- --host"

echo.
echo All services launched!
echo - Access Frontend UI: http://localhost:3000
echo - Access Swagger Docs: http://127.0.0.1:8000/docs
echo - Standalone Production UI: http://127.0.0.1:8000
echo.
pause
