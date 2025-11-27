# CapCut Audio Organizer

Ferramenta profissional para organizar automaticamente clipes de áudio TTS no CapCut.

## ✨ Features

- 🎯 Preview de mudanças antes de processar
- 📜 Histórico dos últimos projetos
- 🎨 Tema claro/escuro
- 🎊 Animações de confete
- 💾 Backup automático
- 🖥️ Interface nativa (macOS)

## 🚀 Como Usar

### Opção 1: Executar diretamente
```bash
./StartApp.command
```

### Opção 2: Criar app bundle
```bash
./build_app.sh
```

## 📦 Estrutura do Projeto

```
├── backend/
│   └── app.py              # Servidor Flask + API
├── templates/
│   └── index.html          # Interface
├── static/
│   ├── style.css           # Estilos
│   └── script.js           # Lógica frontend
├── organize_audio.py       # Core logic
├── StartApp.command        # Launcher
└── build_app.sh           # Build script
```

## 🛠️ Requisitos

- Python 3.8+
- Flask
- pywebview

## 📄 Licença

Criado por Anderson Network

## 🎯 Versão

2.0 - All Features Implemented
