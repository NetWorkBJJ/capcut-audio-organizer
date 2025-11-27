#!/bin/bash
# Script para futuras atualizações (push)

echo "🚀 Fazendo push das mudanças..."
echo ""

# Verificar se há mudanças
if [[ -z $(git status -s) ]]; then
    echo "✓ Nenhuma mudança para commitar"
else
    # Adicionar todas as mudanças
    git add .
    
    # Pedir mensagem de commit
    echo "Digite a mensagem do commit:"
    read commit_message
    
    git commit -m "$commit_message"
fi

# Push
git push

echo ""
echo "✅ Atualizado com sucesso!"
echo "📍 Ver no GitHub: https://github.com/NetWorkBJJ/capcut-audio-organizer"
