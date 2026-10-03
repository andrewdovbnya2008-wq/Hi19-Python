@echo off
setlocal
set "CORE=C:\Hi19CMD\core.py"
if not exist "%CORE%" set "CORE=%~dp0core.py"
where python >nul 2>nul
if not errorlevel 1 goto run_python
where py >nul 2>nul
if not errorlevel 1 goto run_py
echo Python not found. Install it from https://www.python.org/downloads/
exit /b 1
:run_python
python "%CORE%" %*
exit /b %errorlevel%
:run_py
py -3 "%CORE%" %*
exit /b %errorlevel%
