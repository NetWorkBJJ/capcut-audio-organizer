# 🎨 CapCut Audio Organizer

> Ferramenta profissional para organizar automaticamente clipes de áudio TTS no CapCut  
> **v2.1** - 9/9 Features Completas ✅

![App Icon](https://raw.githubusercontent.com/NetWorkBJJ/capcut-audio-organizer/main/.github/icon.png)

---

## ✨ Features

### 🎯 Funcionalidades Core
- **🔍 Preview de Mudanças** - Veja exatamente o que será modificado antes de processar
- **📜 Histórico de Projetos** - Acesso rápido aos últimos 5 projetos editados  
- **💾 Backup Automático** - Todos os arquivos são salvos antes de modificar
- **📦 Batch Processing** - Processe múltiplos projetos de uma vez

### 🎨 Interface Premium
- **🌓 Tema Claro/Escuro** - Alterne entre modos com um clique
- **🎊 Animações de Confete** - Celebração visual ao concluir com sucesso
- **💎 Design Glassmorphism** - Interface moderna com blur effects
- **🖥️ App Nativo** - Janela dedicada (não abre no navegador)

### 🛠️ Técnico
- **⚡ API Nativa** - Comunicação Python ↔ JavaScript via pywebview
- **📝 Sistema de Logs** - Rastreamento de todas as operações
- **🔐 Segurança** - Backups antes de qualquer modificação

---

## 🚀 Instalação Rápida

### Requisitos
- macOS 10.13+
- Python 3.8+

### Opção 1: Executar Diretamente
```bash
# Clone o repositório
git clone https://github.com/NetWorkBJJ/capcut-audio-organizer.git
cd capcut-audio-organizer

# Execute
./StartApp.command
```

### Opção 2: Criar App Bundle
```bash
# Cria CapCut Audio Organizer.app
./build_app.sh

# Mova para Applications
mv "CapCut Audio Organizer.app" /Applications/
```

---

## 📖 Como Usar

### Processar Um Projeto
1. Execute `./StartApp.command`
2. Clique na área de upload
3. Selecione o arquivo `template-2.tmp` do seu projeto CapCut
4. Veja o preview das mudanças
5. Clique em "Processar"
6. Confetes! 🎊

### Processar em Lote
1. Clique no botão **"📦 Processar Lote"**
2. Selecione múltiplos arquivos (Cmd+clique)
3. Aguarde o processamento automático
4. Veja o relatório completo

### Alternar Tema
- Clique no ícone ☀️/🌙 no canto superior direito
- Preferência salva automaticamente

---

## 🏗️ Estrutura do Projeto

```
capcut-audio-organizer/
├── backend/
│   └── app.py              # Flask server + API
├── templates/
│   └── index.html          # UI principal
├── static/
│   ├── style.css           # Estilos com temas
│   └── script.js           # Lógica frontend
├── organize_audio.py       # Core logic + backups
├── StartApp.command        # Launcher
├── build_app.sh           # Criar .app bundle
└── README.md              # Esta documentação
```

---

## 🎯 Como Funciona

O CapCut Audio Organizer:

1. **Lê** o arquivo `template-2.tmp` do seu projeto
2. **Identifica** todos os clipes de áudio TTS
3. **Organiza** sequencialmente sem gaps
4. **Consolida** tudo em uma única faixa
5. **Salva** com backup automático
6. **Limpa** o cache do CapCut para forçar reload

### Segurança
- ✅ Backups criados automaticamente (`.backup`)
- ✅ Nunca sobrescreve backups existentes
- ✅ Timestamps atualizados para forçar CapCut a recarregar

---

## 🔧 Desenvolvimento

### Setup Local
```bash
# Instalar dependências
pip3 install flask pywebview

# Executar em modo dev
python3 backend/app.py
```

### Fazer Mudanças
```bash
# Criar branch
git checkout -b feature/nova-funcionalidade

# Fazer commit
git add .
git commit -m "feat: nova funcionalidade"

# Push
git push origin feature/nova-funcionalidade
```

---

## 📊 Tecnologias

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Desktop:** pywebview (Cocoa WebKit)
- **UI:** Glassmorphism, CSS Variables
- **Libs:** canvas-confetti

---

## 🐛 Troubleshooting

### App não abre
```bash
# Dar permissão de execução
chmod +x StartApp.command
./StartApp.command
```

### Mudanças não aparecem no CapCut
- O script limpa o cache automaticamente
- Se não funcionar, feche e reabra o CapCut
- Verifique se selecionou o arquivo correto (`template-2.tmp`)

### Restaurar backup
```bash
cd "caminho/do/projeto"
mv template-2.tmp.backup template-2.tmp
```

---

## 🗺️ Roadmap Futuro (Opcional)

- [ ] **SaaS Version** - Backend na nuvem + autenticação
- [ ] **Windows/Linux Support** - Multiplataforma
- [ ] **Plugin CapCut** - Integração oficial (se possível)
- [ ] **Mobile App** - iOS/Android
- [ ] **Templates Marketplace** - Compartilhar presets

---

## 📄 Licença

MIT License - Use livremente!

---

## 👨‍💻 Autor

**Anderson Network**

- GitHub: [@NetworkBJJ](https://github.com/NetworkBJJ)
- Projeto: [capcut-audio-organizer](https://github.com/NetWorkBJJ/capcut-audio-organizer)

---

## 🌟 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 🎉 Changelog

### v2.1 (2025-11-27)
- ✨ Batch processing
- ✨ Backup manager API
- ✨ Logging system
- 🎨 UI melhorada com action buttons

### v2.0 (2025-11-27)
- ✨ Preview system
- ✨ Project history
- ✨ Light/dark themes
- ✨ Confetti animations
- 🖥️ Native app (pywebview)

### v1.0
- 🎯 Core audio organization
- 💾 Auto backups
- 🎵 Multi-track support

---

**⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!**

![Made with ❤️ by Anderson Network](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
