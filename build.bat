@echo off
echo ========================================
echo   CapCut Audio Organizer - Build
echo ========================================
echo.

:: Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Instala dependencias
echo Instalando dependencias...
pip install pyinstaller --quiet

:: Gera executavel
echo.
echo Gerando executavel...
pyinstaller --onefile --windowed --name "CapCut Audio Organizer" --add-data "organizer.py;." main.py

echo.
echo ========================================
if exist "dist\CapCut Audio Organizer.exe" (
    echo SUCESSO! Executavel criado em:
    echo dist\CapCut Audio Organizer.exe
) else (
    echo ERRO ao criar executavel!
)
echo ========================================
echo.
pause
