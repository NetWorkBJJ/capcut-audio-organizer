# 🪟 CapCut Audio Organizer - Windows

> Versão Windows do CapCut Audio Organizer v2.1

---

## 📥 Instalação

### Requisitos
- Windows 10/11
- Python 3.8+ ([Download](https://www.python.org/downloads/))

### Passo a Passo

1. **Baixe o projeto**
   ```cmd
   git clone https://github.com/NetWorkBJJ/capcut-audio-organizer.git
   cd capcut-audio-organizer
   ```

2. **Instale dependências**
   
   Clique duas vezes em: `install_windows.bat`
   
   OU execute no CMD:
   ```cmd
   install_windows.bat
   ```

3. **Pronto!**

---

## 🚀 Como Usar

### Executar o App

**Opção 1:** Clique duas vezes em `StartApp.bat`

**Opção 2:** Execute no CMD:
```cmd
StartApp.bat
```

### Localização dos Projetos CapCut

No Windows, os projetos ficam em:
```
C:\Users\SEU_USUARIO\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft
```

O app já abre automaticamente nessa pasta! 🎯

---

## 🎨 Features

Todas as 9 features funcionam no Windows:
- ✅ Preview de mudanças
- ✅ Histórico de projetos
- ✅ Batch processing
- ✅ Backup automático
- ✅ Tema claro/escuro
- ✅ Confetti animations
- ✅ Logs detalhados

---

## 🐛 Troubleshooting

### Python não encontrado
```
[ERROR] Python nao encontrado!
```

**Solução:**
1. Instale Python em: https://www.python.org/downloads/
2. **IMPORTANTE:** Marque "Add Python to PATH" na instalação
3. Reinicie o CMD

### pywebview não funciona
```
[ERROR] Falha ao instalar pywebview
```

**Solução:**
```cmd
pip install --upgrade pip
pip install pywebview[qt]
```

### Porta 5000 em uso
```
Address already in use
```

**Solução:**
```cmd
netstat -ano | findstr :5000
taskkill /PID [número_do_processo] /F
```

---

## 📁 Estrutura

```
capcut-audio-organizer/
├── StartApp.bat              ← Launcher Windows
├── install_windows.bat       ← Instalador Windows
├── backend/
│   └── app.py               ← Servidor (cross-platform)
├── templates/
│   └── index.html           ← Interface
├── static/
│   ├── style.css
│   └── script.js
└── organize_audio.py        ← Core logic
```

---

## 🔄 Diferenças macOS vs Windows

| Feature | macOS | Windows |
|---------|-------|---------|
| Launcher | `.command` | `.bat` |
| CapCut Path | `~/Movies/CapCut/...` | `%LOCALAPPDATA%\CapCut\...` |
| Python | `python3` | `python` |
| App Bundle | `.app` disponível | Executável planejado |

---

## 🎯 Criar Executável (Opcional)

Para criar um `.exe`:

```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico backend/app.py
```

O `.exe` estará em `dist/app.exe`

---

## 📝 Logs

Logs são salvos em:
```
C:\Users\SEU_USUARIO\.capcut_organizer\logs\app.log
```

---

## 🆘 Suporte

- GitHub Issues: https://github.com/NetWorkBJJ/capcut-audio-organizer/issues
- Documentação: [README.md](README.md)

---

**Criado por Anderson Network** ⚡
