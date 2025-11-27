#!/bin/bash
# Installation script for CapCut Audio Organizer
# Created by Anderson Network

echo "🎨 CapCut Audio Organizer - Instalação"
echo "======================================"
echo ""

# Check Python version
echo "📋 Verificando requisitos..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Instale em: https://python.org"
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado!"
    exit 1
fi

echo ""
echo "📦 Instalando dependências..."

# Install Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "   → Instalando Flask..."
    pip3 install flask --quiet
else
    echo "   ✓ Flask já instalado"
fi

# Install pywebview
if ! python3 -c "import webview" 2>/dev/null; then
    echo "   → Instalando pywebview..."
    pip3 install pywebview --quiet
else
    echo "   ✓ pywebview já instalado"
fi

echo ""
echo "🔧 Configurando permissões..."
chmod +x StartApp.command
chmod +x OrganizarAudio.command
chmod +x build_app.sh
chmod +x push_to_github.sh

echo ""
echo "✅ Instalação completa!"
echo ""
echo "🚀 Para executar:"
echo "   ./StartApp.command"
echo ""
echo "📦 Para criar app bundle:"
echo "   ./build_app.sh"
echo ""
echo "Aproveite! 🎉"
