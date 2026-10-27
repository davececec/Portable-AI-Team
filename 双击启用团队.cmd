@echo off
setlocal
chcp 65001 >nul
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0AI-Team\launch.ps1" enable
set "CODE=%ERRORLEVEL%"
echo.
pause
exit /b %CODE%
