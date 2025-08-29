# Script PowerShell para configurar o repositório Git - RAG Chatbot ICTA
# Execute: powershell -ExecutionPolicy Bypass -File setup_git.ps1

Write-Host "🚀 Configurando Repositório Git - RAG Chatbot ICTA" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Verificar se estamos na pasta correta
if (!(Test-Path "rag_chatbot_icta.py")) {
    Write-Host "❌ Erro: Execute este script na pasta do projeto" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Inicializando repositório Git..." -ForegroundColor Yellow
git init

Write-Host "📝 Configurando informações do autor..." -ForegroundColor Yellow
git config user.name "Jesse Fernandes"
git config user.email "jesse.fernandes@ictatechnology.com"

Write-Host "📋 Adicionando arquivos ao repositório..." -ForegroundColor Yellow
git add .

Write-Host "💾 Fazendo commit inicial..." -ForegroundColor Yellow
$commitMessage = @"
🎉 Commit inicial: RAG Chatbot ICTA Technology

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
✅ Testes unitários
"@

git commit -m $commitMessage

Write-Host "🌐 Adicionando remote do GitHub..." -ForegroundColor Yellow
git remote add origin https://github.com/jesseff20/rag-chatbot.git

Write-Host "📊 Status do repositório:" -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "✅ Repositório configurado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Crie o repositório no GitHub: https://github.com/new" -ForegroundColor White
Write-Host "   - Nome: rag-chatbot" -ForegroundColor Gray
Write-Host "   - Descrição: RAG Chatbot para FAQ usando FAISS e modelos locais" -ForegroundColor Gray
Write-Host "   - Público ou Privado (sua escolha)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Envie o código para o GitHub:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configure branch protection (opcional):" -ForegroundColor White
Write-Host "   - Acesse: Settings > Branches no GitHub" -ForegroundColor Gray
Write-Host "   - Adicione regra para main branch" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Links úteis:" -ForegroundColor Cyan
Write-Host "   • Repositório: https://github.com/jesseff20/rag-chatbot" -ForegroundColor Blue
Write-Host "   • Issues: https://github.com/jesseff20/rag-chatbot/issues" -ForegroundColor Blue
Write-Host "   • Releases: https://github.com/jesseff20/rag-chatbot/releases" -ForegroundColor Blue

Write-Host ""
Write-Host "💡 Comandos úteis:" -ForegroundColor Yellow
Write-Host "   git status          # Ver status do repositório" -ForegroundColor Gray
Write-Host "   git add .           # Adicionar todos os arquivos" -ForegroundColor Gray
Write-Host "   git commit -m 'msg' # Fazer commit" -ForegroundColor Gray
Write-Host "   git push            # Enviar para GitHub" -ForegroundColor Gray
Write-Host "   git pull            # Baixar atualizações" -ForegroundColor Gray
