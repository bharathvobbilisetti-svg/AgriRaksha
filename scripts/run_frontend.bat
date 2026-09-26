@echo off
echo =========================================================================
echo   Starting AgriRaksha React Frontend Dev Server (Port 3000)
echo =========================================================================
cd /d "%~dp0\..\frontend"
npm run dev -- --host
pause
