# RAG Chatbot ICTA Technology - Versão Simplificada 🤖✨

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-jesseff20%2Frag--chatbot-black.svg?logo=github)](https://github.com/jesseff20/rag-chatbot)
[![ICTA Technology](https://img.shields.io/badge/ICTA-Technology-orange.svg)](https://ictatechnology.com)

**Sistema RAG com Interface Totalmente Interativa - Agora Qualquer Pessoa Pode Usar!**

> 🎉 **Nova Versão 2.0**: Interface completamente redesenhada com menus interativos coloridos. Não precisa mais decorar comandos - tudo é visual e autoexplicativo!

---

## ✨ Por Que a Versão Simplificada é Melhor?

| 🔴 **Versão Antiga (CLI)** | 🟢 **Nova Versão (Interativa)** |
|---------------------------|----------------------------------|
| Comandos complexos na linha de comando | Menus coloridos e interativos |
| Precisava decorar parâmetros | Explicações em cada opção |
| Difícil para iniciantes | Qualquer pessoa consegue usar |
| Erros sem explicação clara | Ajuda integrada e guias passo-a-passo |
| Interface técnica | Interface amigável e visual |

## 🎯 Características da Nova Interface

### 🎨 **Menus Coloridos e Intuitivos**
- **Verde**: Sucesso e confirmações
- **Azul**: Informações e processamento  
- **Amarelo**: Alertas e dicas importantes
- **Vermelho**: Erros com soluções claras
- **Ciano**: Títulos e navegação

### 📚 **Sistema de Ajuda Completo**
- **Como começar**: Guia passo-a-passo para iniciantes
- **Preparar documentos**: Como organizar seus arquivos
- **Solução de problemas**: Erros comuns e como resolver
- **Dicas avançadas**: Como obter melhores resultados
- **Sobre o projeto**: Informações técnicas detalhadas

### 🔍 **Status em Tempo Real**
- Verifica automaticamente se tudo está funcionando
- Mostra quantos documentos foram carregados
- Informa o status do índice de busca
- Dá recomendações personalizadas

### ⚙️ **Configurações Visuais**
- Veja todas as configurações atuais
- Entenda o que cada parâmetro faz
- Dicas para otimizar performance

## 🚀 Menu Principal - Super Simples!

Quando você executa o programa, vê este menu intuitivo:

```
🤖 RAG Chatbot ICTA Technology - Versão Simplificada
====================================================

📋 MENU PRINCIPAL

 1. 🏗️ Construir Base de Conhecimento
    Processa seus arquivos .txt e cria o índice de busca

 2. 💬 Iniciar Chat Interativo  
    Conversa com o chatbot usando a base criada

 3. 📊 Verificar Status do Sistema
    Mostra informações sobre arquivos e configurações

 4. ⚙️ Configurações
    Ajustar parâmetros básicos do sistema

 5. 📚 Ajuda
    Guias, exemplos e solução de problemas

 6. 🚪 Sair
    Encerra o programa

🎯 Escolha uma opção (1-6):
```

## 🛠️ Instalação Super Fácil

### 📥 **Passo 1: Baixar o Projeto**

```bash
# Opção A: Git (recomendado)
git clone https://github.com/jesseff20/rag-chatbot.git
cd rag-chatbot

# Opção B: Download direto
# Baixe o ZIP do GitHub e extraia
```

### 🐍 **Passo 2: Instalar Python e Dependências**

```bash
# Instalar automaticamente (recomendado)
python setup.py install

# OU instalar manualmente
pip install -r requirements.txt
```

### 🚀 **Passo 3: Executar o Programa**

```bash
python rag_chatbot_icta.py
```

**É só isso!** O programa abre com a interface interativa.

## 📁 Como Preparar Seus Documentos

### 📂 **Estrutura Simples**
```
data/
├── faq_geral.txt
├── produtos.txt  
├── suporte.txt
└── politicas.txt
```

### 📝 **Formato dos Arquivos .txt**
```
P: Como funciona o sistema?
R: Nosso sistema utiliza inteligência artificial para...

P: Quais são os preços?
R: Oferecemos planos a partir de R$ 99/mês...

P: Como entrar em contato?
R: Entre em contato pelo WhatsApp (11) 99999-9999...
```

### 💡 **Dicas Importantes**
- ✅ Use perguntas que seus clientes realmente fazem
- ✅ Respostas claras e diretas
- ✅ Inclua palavras-chave importantes
- ✅ Organize por temas em arquivos separados
- ❌ Evite textos muito longos
- ❌ Não use informações desatualizadas

## 🎯 Como Usar - Passo a Passo Completo

### **1️⃣ Primeira Execução**
1. Execute `python rag_chatbot_icta.py`
2. Escolha opção `3 - Verificar Status` para ver o que precisa
3. O sistema te guiará sobre o que fazer

### **2️⃣ Preparar Documentos**  
1. Crie a pasta `data` (ou use a existente)
2. Adicione seus arquivos .txt com formato P: pergunta R: resposta
3. Escolha opção `5 - Ajuda > 2 - Preparar documentos` para ver exemplos

### **3️⃣ Construir Base de Conhecimento**
1. Escolha opção `1 - Construir Base de Conhecimento`
2. O sistema mostrará quantos arquivos encontrou
3. Confirme e aguarde o processamento (primeira vez demora mais)

### **4️⃣ Conversar com o Chatbot**
1. Escolha opção `2 - Iniciar Chat Interativo`
2. Digite suas perguntas naturalmente
3. Use comandos especiais:
   - `help` - ajuda do chat
   - `status` - últimas conversas
   - `sair` - voltar ao menu

### **5️⃣ Monitorar e Melhorar**
1. Use `3 - Status` para ver estatísticas
2. Teste com perguntas reais
3. Adicione mais documentos conforme necessário
4. Reconstrua a base após mudanças

## 🔧 Tecnologias e Requisitos

### 🐍 **Python e Dependências**
- **Python 3.8+** (obrigatório)
- **FAISS**: Busca vetorial Facebook AI
- **Sentence Transformers**: Embeddings de texto
- **FLAN-T5**: Modelo de linguagem Google
- **Colorama**: Interface colorida
- **Torch**: Framework de deep learning

### 💾 **Requisitos do Sistema**
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **Espaço**: ~2GB para modelos
- **Internet**: Apenas para download inicial
- **OS**: Windows, Linux, macOS

### ⚡ **Performance**
- **Primeira execução**: 5-15 minutos (download de modelos)
- **Construção da base**: 1-10 minutos (depende do tamanho)
- **Chat**: Respostas em 2-10 segundos
- **Funcionamento**: 100% offline após configuração

## 🆘 Solução de Problemas Comum

### ❌ **"Nenhum arquivo .txt encontrado"**
```bash
# Solução:
1. Verifique se a pasta 'data' existe
2. Confirme que há arquivos .txt na pasta  
3. Use a opção 5 - Ajuda para ver exemplos
```

### ❌ **"Erro de memória"**
```bash
# Solução:
1. Feche outros programas pesados
2. Use chunks menores (edite o código)
3. Considere um modelo menor (flan-t5-small)
```

### ❌ **"Respostas ruins"**
```bash
# Solução:
1. Melhore a qualidade dos documentos
2. Use textos mais específicos
3. Adicione mais exemplos similares
4. Verifique se as palavras-chave estão corretas
```

### ❌ **"Modelo não encontrado"**
```bash
# Solução:
1. Verifique sua conexão com internet
2. Aguarde o download (pode demorar na primeira vez)
3. Tente novamente após alguns minutos
```

## 📊 Estrutura do Projeto

```
rag-chatbot/
├── 📄 rag_chatbot_icta.py        # Programa principal (interface interativa)
├── 📄 requirements.txt           # Dependências Python
├── 📄 setup.py                   # Instalador automático
├── 📄 README.md                  # Este arquivo
├── 📁 data/                      # Seus documentos .txt
│   ├── faq_geral_icta.txt
│   ├── integracoes_totvs.txt
│   └── ...
├── 📁 index/                     # Índices gerados automaticamente
│   ├── faiss.index
│   ├── meta.jsonl
│   └── settings.json
├── 📁 history/                   # Histórico de conversas
├── 📁 tests/                     # Testes automatizados
└── 📁 docs/                      # Documentação adicional
```

## 🤝 Contribuindo

Quer ajudar a melhorar o projeto? Ficamos felizes!

### 🐛 **Reportar Problemas**
- Use o [GitHub Issues](https://github.com/jesseff20/rag-chatbot/issues)
- Descreva o problema detalhadamente
- Inclua prints se possível

### 💡 **Sugerir Melhorias**
- Abra um [GitHub Discussion](https://github.com/jesseff20/rag-chatbot/discussions)
- Explique sua ideia
- Cite casos de uso

### 🔧 **Contribuir com Código**
- Faça um fork do projeto
- Crie uma branch para sua feature
- Envie um Pull Request

## 📞 Suporte e Contato

### 🆘 **Precisa de Ajuda?**
1. **GitHub Issues**: [Reportar problemas](https://github.com/jesseff20/rag-chatbot/issues)
2. **Discussões**: [GitHub Discussions](https://github.com/jesseff20/rag-chatbot/discussions)  
3. **Email**: contato@ictatechnology.com
4. **Sistema de Ajuda**: Use a opção 5 no menu do programa

### 👨‍💻 **Sobre o Desenvolvedor**
- **Nome**: Jesse Fernandes
- **Empresa**: ICTA Technology
- **GitHub**: [@jesseff20](https://github.com/jesseff20)
- **Email**: jesse.fernandes@ictatechnology.com

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 🎁 **O que isso significa?**
- ✅ Uso comercial permitido
- ✅ Modificação permitida  
- ✅ Distribuição permitida
- ✅ Uso privado permitido
- ⚠️ Sem garantia

## 🙏 Agradecimentos

- **FAISS Team**: Biblioteca de busca vetorial fantástica
- **Hugging Face**: Modelos e ferramentas incríveis
- **Sentence Transformers**: Embeddings de qualidade
- **Google**: Modelo FLAN-T5 open-source
- **Comunidade Python**: Ecossistema incrível

---

## 🚀 Changelog da Versão 2.0

### ✨ **Novidades**
- **Interface Totalmente Interativa**: Menus coloridos substituem linha de comando
- **Sistema de Ajuda Integrado**: Guias completos dentro do programa
- **Status em Tempo Real**: Verificação automática de configuração
- **Melhor Experiência**: Explicações em cada opção
- **Detecção de Problemas**: Identifica e sugere soluções

### 🔧 **Melhorias**
- **Performance**: Processamento mais rápido
- **Estabilidade**: Tratamento melhor de erros
- **Usabilidade**: Interface muito mais amigável
- **Documentação**: README completamente reescrito
- **Compatibilidade**: Funciona melhor no Windows

### 🐛 **Correções**
- Problemas com encoding de caracteres
- Erros de path no Windows
- Travamentos durante processamento
- Mensagens de erro confusas

---

**💝 Desenvolvido com ❤️ para tornar IA acessível a todos!**

*Se este projeto te ajudou, considere dar uma ⭐ no GitHub!*
