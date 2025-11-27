@echo off
REM CapCut Audio Organizer - Windows Launcher
REM Created by Anderson Network

echo.
echo ========================================
echo   CapCut Audio Organizer v2.1
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python nao encontrado!
    echo Por favor, instale Python em: https://python.org
    pause
    exit /b 1
)

REM Check and install Flask
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Instalando Flask...
    pip install flask
)

REM Check and install pywebview
python -c "import webview" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Instalando pywebview...
    pip install pywebview
)

echo [INFO] Iniciando aplicacao...
echo.

REM Run the app
python backend\app.py

pause
