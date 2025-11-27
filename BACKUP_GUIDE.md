# 📚 Guia de Backup e Git

## ✅ Status Atual

**Git inicializado com sucesso!**
- ✓ Repositório criado
- ✓ .gitignore configurado
- ✓ README.md criado
- ✓ Primeiro commit feito

---

## 🔄 Sistema de Backup Automático

O app já possui backup integrado que funciona assim:

### Como Funciona
```
Ao processar um projeto:
1. Verifica se .backup existe
2. Se NÃO existe → Cria backup
3. Se existe → Pula (preserva backup original)
4. Processa o arquivo
```

### Localização dos Backups
```
~/Movies/CapCut/User Data/Projects/com.lveditor.draft/[seu_projeto]/
├── template-2.tmp
├── template-2.tmp.backup           ← Backup automático
├── draft_info.json
├── draft_info.json.backup          ← Backup automático
└── draft_meta_info.json.backup     ← Backup automático
```

### Restaurar um Backup
```bash
# Se algo der errado, simplesmente renomeie:
cd "caminho/do/projeto"
mv template-2.tmp.backup template-2.tmp
```

---

## 🐙 Próximos Passos - Git

### 1. Criar Repositório no GitHub

**Opção A: Via Site**
1. Acesse https://github.com/new
2. Nome: `capcut-audio-organizer`
3. Descrição: `Professional tool to organize TTS audio clips in CapCut`
4. Público ou Privado (sua escolha)
5. **NÃO** marque "Initialize with README"
6. Crie o repositório

**Opção B: Via GitHub CLI**
```bash
# Se tiver gh instalado
gh repo create capcut-audio-organizer --public --source=. --remote=origin
```

### 2. Conectar e Fazer Push

```bash
# Adicionar remote (copie a URL do GitHub)
git remote add origin https://github.com/SEU-USUARIO/capcut-audio-organizer.git

# Renomear branch para main (padrão moderno)
git branch -M main

# Fazer primeiro push
git push -u origin main
```

---

## 📝 Comandos Git Úteis

### Comandos Diários
```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Commit
git commit -m "descrição das mudanças"

# Push para GitHub
git push

# Ver histórico
git log --oneline --graph
```

### Criar uma Tag de Versão
```bash
# Marcar versão 2.0
git tag -a v2.0 -m "Version 2.0 - All features"
git push origin v2.0
```

### Branches para Novas Features
```bash
# Criar branch para SaaS
git checkout -b feature/saas-backend

# Trabalhar na feature...

# Voltar para main
git checkout main

# Merge da feature
git merge feature/saas-backend
```

---

## 🔐 Gerenciar Backups Manualmente

### Ver Backups
```bash
# Listar todos os backups do CapCut
find ~/Movies/CapCut -name "*.backup" -type f
```

### Criar Backup Manual
```bash
# Antes de fazer algo arriscado
cd "/caminho/do/projeto"
cp -r . "../backup-$(date +%Y%m%d-%H%M%S)"
```

### Limpar Backups Antigos (>7 dias)
```bash
find ~/Movies/CapCut -name "*.backup" -mtime +7 -delete
```

---

## 💡 Workflow Recomendado

### Para Desenvolvimento
```bash
# 1. Criar branch
git checkout -b feature/nova-funcionalidade

# 2. Fazer mudanças
# ... editar arquivos ...

# 3. Commit frequente
git add .
git commit -m "feat: adiciona feature X"

# 4. Push
git push -u origin feature/nova-funcionalidade

# 5. Criar Pull Request no GitHub
```

### Para Versionar Releases
```bash
# Quando tiver versão estável
git tag -a v2.1 -m "Adicionado SaaS backend"
git push origin v2.1

# Criar release no GitHub
gh release create v2.1 --title "Version 2.1" --notes "Changelog..."
```

---

## 🎯 Comandos Executados (Resumo)

```bash
✓ git init                          # Inicializado
✓ git config user.name              # Configurado
✓ git add .                         # Arquivos adicionados
✓ git commit -m "..."               # Primeiro commit
```

**Próximo passo:**
```bash
git remote add origin <URL_DO_GITHUB>
git push -u origin main
```

---

## 🚨 IMPORTANTE: Nunca Versionar

Já está no `.gitignore`:
- ❌ `*.backup` - Backups locais
- ❌ `*.tmp` - Arquivos temporários
- ❌ `textReading/` - Arquivos de áudio de teste
- ❌ `draft_info.json` - Dados de projeto específico
- ❌ `__pycache__/` - Cache Python

---

## 📊 Status Atual do Git

```
Commit: 1782660
Mensagem: feat: CapCut Audio Organizer v2.0
Arquivos: 10 arquivos (1436 linhas)
Branch: master (pronto para renomear para main)
```

**Pronto para fazer push! 🚀**
