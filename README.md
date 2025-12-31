# CapCut Audio Organizer

Ferramenta para reorganizar audios TTS (Text-to-Speech) do CapCut em uma unica trilha sequencial.

## Problema que resolve

Quando voce usa a funcao Text-to-Speech do CapCut para gerar multiplos audios de narracao, o CapCut os coloca em trilhas de audio separadas e fora de ordem cronologica. Esta ferramenta:

1. Le o arquivo de projeto do CapCut (JSON)
2. Identifica todos os segmentos de audio gerados por TTS
3. Reorganiza-os em uma UNICA trilha de audio
4. Ajusta os tempos de inicio para que fiquem em sequencia
5. Salva o projeto modificado

## Como usar

### Opcao 1: Executavel (Recomendado)

1. Baixe o arquivo `CapCut Audio Organizer.exe` da pasta `dist/`
2. Execute o programa
3. Clique em "Selecionar Arquivo"
4. Navegue ate a pasta do seu projeto CapCut:
   - Caminho padrao: `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\`
   - Procure pelo arquivo `draft_content.json` ou `template-2.tmp`
5. Verifique o preview dos clips que serao reorganizados
6. Clique em "Organizar Audios"
7. Reabra o projeto no CapCut

### Opcao 2: Executar com Python

```bash
# Clone o repositorio
git clone https://github.com/seu-usuario/capcut-audio-organizer.git
cd capcut-audio-organizer

# Execute o programa
python main.py
```

## Gerar executavel

Para gerar o arquivo .exe:

```bash
# Windows
build.bat

# Ou manualmente
pip install pyinstaller
pyinstaller --onefile --windowed --name "CapCut Audio Organizer" main.py
```

O executavel sera criado em `dist/CapCut Audio Organizer.exe`

## Requisitos

- Windows 10/11
- Python 3.8+ (apenas se for executar via script)
- CapCut Desktop instalado

## Estrutura do projeto

```
CapCut Audio Organizer/
├── main.py           # Interface grafica (Tkinter)
├── organizer.py      # Logica de organizacao
├── requirements.txt  # Dependencias
├── build.bat         # Script para gerar .exe
└── README.md         # Este arquivo
```

## Observacoes importantes

- **SEMPRE** feche o projeto no CapCut antes de usar esta ferramenta
- A ferramenta modifica diretamente o arquivo do projeto
- Recomenda-se fazer backup do projeto antes de usar
- Apos organizar, reabra o projeto no CapCut para ver as alteracoes

## Criado por

Anderson Network
