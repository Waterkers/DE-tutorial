@echo off
rem Windows: double-click to start the DE practical.
chcp 65001 >nul
cd /d "%~dp0"
set PRACTICAL_LANG=en
docker info >nul 2>&1 || (echo Docker is not running. Start Docker Desktop and try again. & pause & exit /b 1)
echo Starting the practical (the first start can take a minute)...
docker compose up -d --no-build || (pause & exit /b 1)
powershell -NoProfile -Command "for ($i = 0; $i -lt 60; $i++) { try { Invoke-WebRequest -UseBasicParsing http://localhost:8889/api | Out-Null; exit 0 } catch { Start-Sleep 1 } }; exit 1"
if errorlevel 1 (echo JupyterLab did not start. Show the error with: docker compose logs & pause & exit /b 1)
start "" http://localhost:8889/lab/tree/practical/en
echo Ready: http://localhost:8889 - to stop, double-click stop.bat
pause
