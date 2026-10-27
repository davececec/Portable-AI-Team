@echo off
setlocal
chcp 65001 >nul
if "%~1"=="" goto prompt

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0AI-Team\launch.ps1" merge --other "%~1"
set "CODE=%ERRORLEVEL%"
echo.
pause
exit /b %CODE%

:prompt
echo 请把另一个 Portable-AI-Team 文件夹拖到本窗口后按 Enter。
set /p "OTHER=来源团队路径: "
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0AI-Team\launch.ps1" merge --other "%OTHER%"
set "CODE=%ERRORLEVEL%"
echo.
pause
exit /b %CODE%
