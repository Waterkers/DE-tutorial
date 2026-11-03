@echo off
rem Windows: double-click to stop the practical. Notebooks stay in practical\.
cd /d "%~dp0"
docker compose down
pause
