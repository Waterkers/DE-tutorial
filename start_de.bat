@echo off
rem Windows: double-click to start the DE practical.
chcp 65001 >nul
cd /d "%~dp0"
set PRACTICAL_LANG=de
docker info >nul 2>&1 || (echo Docker läuft nicht. Starte Docker Desktop und versuche es noch einmal. & pause & exit /b 1)
echo Das Praktikum wird gestartet (der erste Start kann eine Minute dauern)...
docker compose up -d --no-build || (pause & exit /b 1)
powershell -NoProfile -Command "for ($i = 0; $i -lt 60; $i++) { try { Invoke-WebRequest -UseBasicParsing http://localhost:8889/api | Out-Null; exit 0 } catch { Start-Sleep 1 } }; exit 1"
if errorlevel 1 (echo JupyterLab ist nicht gestartet. Fehler anzeigen mit: docker compose logs & pause & exit /b 1)
start "" http://localhost:8889/lab/tree/practical/de
echo Fertig: http://localhost:8889 - zum Beenden stop.bat doppelklicken
pause
