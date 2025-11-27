@echo off
REM Installation script for Windows
REM CapCut Audio Organizer

echo.
echo ========================================
echo   Instalacao - CapCut Audio Organizer
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.8+ em:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Marque "Add Python to PATH" durante a instalacao!
    pause
    exit /b 1
)

echo [OK] Python instalado
python --version

echo.
echo [INFO] Instalando dependencias...
echo.

REM Install Flask
echo [1/2] Instalando Flask...
pip install flask
if %errorlevel% neq 0 (
    echo [ERROR] Falha ao instalar Flask
    pause
    exit /b 1
)

REM Install pywebview
echo [2/2] Instalando pywebview...
pip install pywebview
if %errorlevel% neq 0 (
    echo [ERROR] Falha ao instalar pywebview
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Instalacao Completa!
echo ========================================
echo.
echo Para executar o aplicativo:
echo   1. Clique duas vezes em StartApp.bat
echo   OU
echo   2. Execute: StartApp.bat
echo.
pause
