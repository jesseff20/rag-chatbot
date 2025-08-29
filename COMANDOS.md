# 🚀 Guia Rápido - RAG Chatbot ICTA Technology (Versão Simplificada)

> 📍 **Versão 2.0**: Agora com interface totalmente interativa! Não precisa mais decorar comandos.

## ⚡ Execução Simples

```bash
# Execute o programa
python rag_chatbot_icta.py

# O menu interativo será exibido automaticamente!
```

## 🎯 Menu Principal - O que Cada Opção Faz

### 1️⃣ **🏗️ Construir Base de Conhecimento**
- **O que faz**: Lê seus arquivos .txt e cria o índice de busca
- **Quando usar**: Primeira vez ou quando adicionar novos documentos
- **Tempo**: 1-10 minutos (dependendo da quantidade de texto)

### 2️⃣ **💬 Iniciar Chat Interativo**
- **O que faz**: Abre o chat para conversar com o bot
- **Quando usar**: Depois de criar a base de conhecimento
- **Comandos no chat**:
  - `help` - Ajuda do chat
  - `status` - Ver últimas conversas
  - `sair` - Voltar ao menu

### 3️⃣ **📊 Verificar Status do Sistema**
- **O que faz**: Mostra se tudo está funcionando
- **Quando usar**: Para diagnosticar problemas ou ver estatísticas
- **Mostra**: Arquivos encontrados, índice criado, configurações

### 4️⃣ **⚙️ Configurações**
- **O que faz**: Exibe configurações atuais do sistema
- **Quando usar**: Para entender como o sistema está configurado
- **Nota**: Para alterar, edite o código (futuras versões terão interface)

### 5️⃣ **📚 Ajuda**
- **O que faz**: Sistema completo de ajuda e tutoriais
- **Submenus**:
  - Como começar
  - Preparar documentos
  - Solução de problemas
  - Dicas de uso
  - Sobre o projeto

### 6️⃣ **🚪 Sair**
- **O que faz**: Encerra o programa
- **Atalho**: Ctrl+C em qualquer momento

## 📁 Comandos de Arquivo (Opcional)

Se preferir usar linha de comando (modo avançado):

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar testes
python -m pytest tests/

# Instalar como pacote
pip install -e .

# Backup do índice
xcopy /E index backup_index

# Limpar arquivos temporários
del /Q index\*.* && del /Q history\*.*
```

## 🔧 Comandos Git

```bash
# Clonar o repositório
git clone https://github.com/jesseff20/rag-chatbot.git

# Atualizar do GitHub
git pull origin main

# Salvar suas alterações
git add .
git commit -m "Atualizei meus documentos"
git push origin main
```

## 🚨 Solução Rápida de Problemas

### ❌ **Programa não inicia**
```bash
# Verificar Python
python --version

# Instalar dependências novamente
pip install -r requirements.txt --force-reinstall
```

### ❌ **Erro "Arquivo não encontrado"**
```bash
# Verificar se está no diretório correto
pwd  # Linux/Mac
cd    # Windows

# Verificar arquivos
ls    # Linux/Mac
dir   # Windows
```

### ❌ **Sem arquivos .txt**
```bash
# Criar pasta data
mkdir data

# Verificar conteúdo
ls data/     # Linux/Mac
dir data\    # Windows
```

## 💡 Dicas Rápidas

### 🎯 **Para Melhores Resultados**
1. Use textos claros no formato "P: pergunta R: resposta"
2. Coloque arquivos .txt na pasta `data/`
3. Reconstrua a base após adicionar documentos
4. Teste com perguntas reais dos usuários

### ⚡ **Para Performance**
- Feche outros programas pesados
- Use SSD se possível
- Primeira execução demora mais (download de modelos)

### 🔄 **Fluxo Típico de Uso**
```
1. Adicionar arquivos .txt em data/
2. Executar: python rag_chatbot_icta.py
3. Escolher: 1 - Construir Base de Conhecimento
4. Escolher: 2 - Iniciar Chat Interativo
5. Conversar com o bot!
```

## 📞 Suporte Rápido

- **Problemas**: Use opção 5 (Ajuda) no menu
- **GitHub**: https://github.com/jesseff20/rag-chatbot/issues
- **Email**: contato@ictatechnology.com

---

💝 **Interface simplificada = mais produtividade para você!**
