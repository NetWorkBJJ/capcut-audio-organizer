#!/bin/bash
cd "$(dirname "$0")"

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install flask
fi

# Check if pywebview is installed
python3 -c "import webview" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências (pywebview)..."
    pip3 install pywebview
fi

# Start App (Native Window)
echo "Iniciando CapCut Audio Organizer..."
python3 backend/app.py
