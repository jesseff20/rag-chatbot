#!/bin/bash
# Script para configurar o repositório Git - RAG Chatbot ICTA
# Execute: bash setup_git.sh

echo "🚀 Configurando Repositório Git - RAG Chatbot ICTA"
echo "=================================================="

# Verificar se estamos na pasta correta
if [ ! -f "rag_chatbot_icta.py" ]; then
    echo "❌ Erro: Execute este script na pasta do projeto"
    exit 1
fi

echo "📁 Inicializando repositório Git..."
git init

echo "📝 Configurando informações do autor..."
git config user.name "Jesse Fernandes"
git config user.email "jesse.fernandes@ictatechnology.com"

echo "📋 Adicionando arquivos ao repositório..."
git add .

echo "💾 Fazendo commit inicial..."
git commit -m "🎉 Commit inicial: RAG Chatbot ICTA Technology

- Implementação completa do sistema RAG
- Suporte a FAISS para busca vetorial
- Modelos locais FLAN-T5
- Sistema de instalação automática
- Testes automatizados
- Documentação completa

Funcionalidades:
✅ Construção de índice vetorial
✅ Chat interativo
✅ Suporte a múltiplos modelos
✅ Histórico de conversas
✅ Instalação automática
✅ Testes unitários"

echo "🌐 Adicionando remote do GitHub..."
git remote add origin https://github.com/jesseff20/rag-chatbot.git

echo "📊 Status do repositório:"
git status

echo ""
echo "✅ Repositório configurado com sucesso!"
echo ""
echo "🚀 Próximos passos:"
echo "1. Crie o repositório no GitHub: https://github.com/new"
echo "   - Nome: rag-chatbot"
echo "   - Descrição: RAG Chatbot para FAQ usando FAISS e modelos locais"
echo "   - Público ou Privado (sua escolha)"
echo ""
echo "2. Envie o código para o GitHub:"
echo "   git push -u origin main"
echo ""
echo "3. Configure branch protection (opcional):"
echo "   - Acesse: Settings > Branches no GitHub"
echo "   - Adicione regra para main branch"
echo ""
echo "📖 Links úteis:"
echo "   • Repositório: https://github.com/jesseff20/rag-chatbot"
echo "   • Issues: https://github.com/jesseff20/rag-chatbot/issues"
echo "   • Releases: https://github.com/jesseff20/rag-chatbot/releases"
