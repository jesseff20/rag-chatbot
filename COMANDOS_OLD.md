# Comandos Rápidos - RAG Chatbot ICTA

## 🚀 Acesso ao Projeto

### GitHub Repository
```bash
# Clone HTTPS
git clone https://github.com/jesseff20/rag-chatbot.git

# Clone SSH
git clone git@github.com:jesseff20/rag-chatbot.git

# Download ZIP
curl -L https://github.com/jesseff20/rag-chatbot/archive/main.zip -o rag-chatbot.zip
```

### Links Importantes
- **Repositório**: https://github.com/jesseff20/rag-chatbot
- **Issues**: https://github.com/jesseff20/rag-chatbot/issues
- **Releases**: https://github.com/jesseff20/rag-chatbot/releases
- **Wiki**: https://github.com/jesseff20/rag-chatbot/wiki

## 📦 Instalação e Configuração

```bash
# Método 1: Instalação automática
git clone https://github.com/jesseff20/rag-chatbot.git
cd rag-chatbot
python install.py

# Método 2: Manual
pip install -r requirements.txt

# Método 3: Como pacote
pip install -e .

# Desenvolvimento
pip install -e ".[dev]"
```

## 🤖 Uso Principal

```bash
# 1. Construir índice
python rag_chatbot_icta.py --build-index --docs-path ./data --index-path ./index/faiss.index --meta-path ./index/meta.jsonl

# 2. Chat básico (FLAN-T5 base)
python rag_chatbot_icta.py --chat --index-path ./index/faiss.index --meta-path ./index/meta.jsonl --generator flan-t5 --model-name google/flan-t5-base

# 3. Chat com modelo maior
python rag_chatbot_icta.py --chat --generator flan-t5 --model-name google/flan-t5-large

# 4. Help completo
python rag_chatbot_icta.py --help
```

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest test_rag_chatbot.py -v

# Teste específico
python -m pytest test_rag_chatbot.py::TestProjectStructure -v

# Testes com cobertura
python -m pytest test_rag_chatbot.py --cov=rag_chatbot_icta --cov-report=html

# Teste rápido de dependências
python -c "import faiss, sentence_transformers, transformers, torch; print('✅ OK')"
```

## 🔧 Desenvolvimento

```bash
# Formatação de código
black *.py

# Linting
flake8 *.py

# Verificação de tipos
mypy rag_chatbot_icta.py

# Verificar setup.py
python setup.py check
python setup.py --name --version --author
```

## 🔄 Git Workflow

### Setup Inicial
```bash
# Configurar Git (primeiro uso)
powershell -ExecutionPolicy Bypass -File setup_git.ps1

# Ou manual
git init
git remote add origin https://github.com/jesseff20/rag-chatbot.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Workflow Diário
```bash
# Verificar status
git status

# Adicionar mudanças
git add .
git add arquivo_especifico.py

# Commit
git commit -m "Descrição das mudanças"

# Push para GitHub
git push

# Pull atualizações
git pull

# Criar branch para feature
git checkout -b feature/nova-funcionalidade
git push -u origin feature/nova-funcionalidade
```

### Contribuição
```bash
# Fork no GitHub primeiro, depois:
git clone https://github.com/SEU_USUARIO/rag-chatbot.git
cd rag-chatbot

# Adicionar upstream
git remote add upstream https://github.com/jesseff20/rag-chatbot.git

# Criar branch para feature
git checkout -b feature/minha-contribuicao

# Fazer mudanças e commit
git add .
git commit -m "Adiciona nova funcionalidade"

# Push e abrir PR
git push origin feature/minha-contribuicao
```

## 🔍 Solução de Problemas

### Dependências
```bash
# Verificar instalação
python -c "import faiss, sentence_transformers, transformers, torch; print('✅ OK')"

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Verificar versões
pip list | grep -E "(torch|transformers|faiss|sentence)"

# Limpar cache
rm -rf __pycache__ .pytest_cache ~/.cache/huggingface/
```

### Git Issues
```bash
# Reset local para remote
git fetch origin
git reset --hard origin/main

# Verificar remotes
git remote -v

# Reconfigurar origin
git remote set-url origin https://github.com/jesseff20/rag-chatbot.git

# Ver histórico
git log --oneline
```

### Sistema
```bash
# Windows PowerShell - Limpar cache
Remove-Item -Recurse -Force __pycache__, .pytest_cache

# Linux/Mac - Limpar cache
rm -rf __pycache__ .pytest_cache

# Verificar Python
python --version
python -c "import sys; print(sys.executable)"

# Verificar pip
pip --version
pip list
```

## 📊 Monitoramento

### Logs e Debug
```bash
# Ver arquivos de log (se existirem)
ls -la *.log
tail -f application.log

# Debug de importações
python -c "
import sys
print('Python:', sys.version)
print('Path:', sys.path[:3])
try:
    import faiss
    print('FAISS: OK')
except Exception as e:
    print('FAISS:', e)
"

# Verificar modelos baixados
ls -la ~/.cache/huggingface/transformers/
```

### Performance
```bash
# Verificar uso de memória
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'RAM: {process.memory_info().rss / 1024 / 1024:.1f} MB')
print(f'CPU: {psutil.cpu_percent()}%')
"

# Benchmark básico
time python rag_chatbot_icta.py --help
```

## 🌐 Recursos Online

### GitHub Actions (CI/CD)
- Automatic testing
- Code quality checks  
- Release automation
- Documentation updates

### Links Úteis
- **Issues**: https://github.com/jesseff20/rag-chatbot/issues
- **Discussions**: https://github.com/jesseff20/rag-chatbot/discussions
- **Actions**: https://github.com/jesseff20/rag-chatbot/actions
- **Insights**: https://github.com/jesseff20/rag-chatbot/pulse

### Badges para README
```markdown
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-jesseff20%2Frag--chatbot-black.svg)](https://github.com/jesseff20/rag-chatbot)
```
