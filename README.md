# RAG Chatbot ICTA Technology 🤖

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-jesseff20%2Frag--chatbot-black.svg)](https://github.com/jesseff20/rag-chatbot)

**Sistema de Chatbot RAG (Retrieval-Augmented Generation) para FAQ usando FAISS e modelos locais**

---

## 🎯 Objetivo

Chatbot simples e eficiente para responder perguntas frequentes usando tecnologia RAG:

- **🔍 Busca Vetorial**: Indexação com FAISS para busca semântica rápida
- **🧠 Embeddings**: Sentence-Transformers para representação de texto
- **🤖 Geração Local**: Modelos open-source (FLAN-T5) sem APIs pagas
- **📚 Conhecimento**: Base de conhecimento personalizável via arquivos .txt
- **💾 Histórico**: Rastreamento opcional de conversas
- **🔧 Flexível**: Suporte a diferentes modelos e configurações

## 🚀 Instalação Rápida

### Método 1: Script Automático (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/jesseff20/rag-chatbot.git
cd rag-chatbot

# Execute o instalador automático
python install.py
```

### Método 2: Instalação Manual

```bash
# Clone o repositório
git clone https://github.com/jesseff20/rag-chatbot.git
cd rag-chatbot

# Instale as dependências
pip install -r requirements.txt

# (Opcional) Instale como pacote
pip install -e .
```

### Método 3: Desenvolvimento

```bash
# Para desenvolvedores
git clone https://github.com/jesseff20/rag-chatbot.git
cd rag-chatbot
pip install -e ".[dev]"
```

## 📁 Estrutura do Projeto

```
rag-chatbot/
├── 📄 rag_chatbot_icta.py      # Script principal do chatbot
├── 📄 requirements.txt         # Dependências do projeto
├── 📄 setup.py                # Configuração de instalação
├── 📄 install.py              # Script de instalação automática
├── 📄 test_rag_chatbot.py     # Testes automatizados
├── 📄 README.md               # Este arquivo
├── 📄 COMANDOS.md             # Comandos rápidos
├── 📄 CONTRIBUTING.md         # Guia de contribuição
├── 📄 LICENSE                 # Licença MIT
├── 📄 .gitignore             # Arquivos ignorados pelo Git
├── 📁 data/                   # Seus arquivos .txt (FAQs/documentos)
│   ├── faq_geral_icta.txt
│   ├── integracoes_totvs.txt
│   ├── politica_respostas.txt
│   └── servicos_bi_automacao_ia.txt
├── 📁 index/                  # Índices FAISS (gerados automaticamente)
│   ├── faiss.index           # (gerado)
│   ├── meta.jsonl            # (gerado)
│   ├── settings.json         # (gerado)
│   └── README.txt
└── 📁 history/               # Histórico de conversas
    ├── chat_history.jsonl   # (gerado)
    └── README.txt
```

## 🛠️ Como Usar

### 1️⃣ Preparar os Dados
Coloque seus arquivos `.txt` com FAQs e documentos no diretório `data/`:

```bash
# Exemplo de estrutura de arquivo .txt
echo "P: Como funciona o sistema de BI?
R: Nosso sistema de BI utiliza tecnologias avançadas..." > data/minha_faq.txt
```

### 2️⃣ Construir o Índice Vetorial
```bash
python rag_chatbot_icta.py --build-index \
    --docs-path ./data \
    --index-path ./index/faiss.index \
    --meta-path ./index/meta.jsonl
```

### 3️⃣ Iniciar o Chat

#### Modo Padrão (FLAN-T5 Base - Recomendado)
```bash
python rag_chatbot_icta.py --chat \
    --index-path ./index/faiss.index \
    --meta-path ./index/meta.jsonl \
    --generator flan-t5 \
    --model-name google/flan-t5-base
```

#### Modelo Maior (Melhor Qualidade)
```bash
python rag_chatbot_icta.py --chat \
    --generator flan-t5 \
    --model-name google/flan-t5-large
```

#### Usando Servidor TGI (Avançado)
```bash
# Para uso com Text Generation Inference
python rag_chatbot_icta.py --chat \
    --generator tgi \
    --tgi-url http://localhost:8080 \
    --system-language pt
```

## 🧪 Testes e Validação

### Executar Testes
```bash
# Todos os testes
python -m pytest test_rag_chatbot.py -v

# Teste específico
python -m pytest test_rag_chatbot.py::TestRAGChatbot::test_imports -v

# Com cobertura
python -m pytest test_rag_chatbot.py --cov=rag_chatbot_icta --cov-report=html
```

### Validar Instalação
```bash
# Verificar dependências
python -c "import faiss, sentence_transformers, transformers, torch; print('✅ Tudo OK!')"

# Teste rápido do sistema
python install.py
```

## ⚙️ Configuração Avançada

### Parâmetros do Sistema

| Parâmetro | Descrição | Padrão |
|-----------|-----------|---------|
| `--chunk-size` | Tamanho dos chunks de texto | 800 |
| `--overlap` | Sobreposição entre chunks | 120 |
| `--top-k` | Número de documentos similares | 3 |
| `--embedding-model` | Modelo de embeddings | all-MiniLM-L6-v2 |
| `--max-tokens` | Tokens máximos na resposta | 150 |

### Exemplo com Parâmetros Customizados
```bash
python rag_chatbot_icta.py --build-index \
    --docs-path ./data \
    --chunk-size 600 \
    --overlap 100 \
    --embedding-model sentence-transformers/all-mpnet-base-v2
```

## 🔧 Desenvolvimento

### Configurar Ambiente de Desenvolvimento
```bash
# Clone e configure
git clone https://github.com/jesseff20/rag-chatbot.git
cd rag-chatbot
pip install -e ".[dev]"

# Ferramentas de desenvolvimento
black *.py                    # Formatação
flake8 *.py                   # Linting
mypy rag_chatbot_icta.py     # Verificação de tipos
```

### Contribuir para o Projeto
1. **Fork** o repositório no GitHub
2. **Clone** seu fork: `git clone https://github.com/SEU_USUARIO/rag-chatbot.git`
3. **Crie uma branch**: `git checkout -b feature/nova-funcionalidade`
4. **Faça suas alterações** e adicione testes
5. **Execute os testes**: `python -m pytest`
6. **Commit**: `git commit -am 'Adiciona nova funcionalidade'`
7. **Push**: `git push origin feature/nova-funcionalidade`
8. **Abra um Pull Request**

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes completos.

## 📊 Requisitos do Sistema

### Software
- **Python**: 3.8 ou superior
- **Memória RAM**: Mínimo 4GB (recomendado 8GB+)
- **Espaço em Disco**: 2GB para modelos e dependências

### Dependências Principais
- `faiss-cpu` - Busca vetorial eficiente
- `sentence-transformers` - Modelos de embedding
- `transformers` - Modelos de linguagem
- `torch` - Framework de deep learning
- `numpy` - Computação numérica
- `tqdm` - Barras de progresso
- `colorama` - Interface colorida
- `requests` - Cliente HTTP

## 🌐 Acessar o Projeto

### GitHub Repository
- **URL**: https://github.com/jesseff20/rag-chatbot
- **Clone HTTPS**: `git clone https://github.com/jesseff20/rag-chatbot.git`
- **Clone SSH**: `git clone git@github.com:jesseff20/rag-chatbot.git`

### Links Úteis
- **Issues**: https://github.com/jesseff20/rag-chatbot/issues
- **Releases**: https://github.com/jesseff20/rag-chatbot/releases
- **Wiki**: https://github.com/jesseff20/rag-chatbot/wiki
- **Discussions**: https://github.com/jesseff20/rag-chatbot/discussions

### Download Direct
```bash
# Última versão via curl
curl -L https://github.com/jesseff20/rag-chatbot/archive/main.zip -o rag-chatbot.zip
unzip rag-chatbot.zip
cd rag-chatbot-main

# Ou usando wget
wget https://github.com/jesseff20/rag-chatbot/archive/main.zip
```

## ❓ Solução de Problemas

### Problemas Comuns

#### Erro de Memória
```bash
# Use modelo menor
python rag_chatbot_icta.py --chat --model-name google/flan-t5-small
# Ou reduza chunk_size
python rag_chatbot_icta.py --build-index --chunk-size 400
```

#### Modelos Não Baixam
```bash
# Limpe o cache
rm -rf ~/.cache/huggingface/
# Tente novamente
python rag_chatbot_icta.py --chat
```

#### Problemas de Dependências
```bash
# Reinstale tudo
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
# Ou use o instalador
python install.py
```

### Logs e Debug
```bash
# Modo verbose (se implementado)
python rag_chatbot_icta.py --chat --verbose

# Verificar versões
pip list | grep -E "(torch|transformers|faiss|sentence)"
```

## 📈 Roadmap

### Versão 1.1
- [ ] Interface web opcional
- [ ] Suporte a PDF e DOCX
- [ ] Cache inteligente de embeddings
- [ ] Métricas de qualidade das respostas

### Versão 1.2
- [ ] Suporte a múltiplos idiomas
- [ ] API REST
- [ ] Docker containers
- [ ] Integração com Slack/Discord

### Versão 2.0
- [ ] Fine-tuning automático
- [ ] RAG hierárquico
- [ ] Suporte a bases de dados vetoriais
- [ ] Dashboard de analytics

## 🤝 Contribuições

Contribuições são muito bem-vindas! Veja como ajudar:

1. **Reportar Bugs**: [Abra uma issue](https://github.com/jesseff20/rag-chatbot/issues)
2. **Sugerir Features**: [Discussions](https://github.com/jesseff20/rag-chatbot/discussions)
3. **Contribuir Código**: Veja [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Melhorar Docs**: PRs para documentação são muito apreciados
5. **Compartilhar**: Star ⭐ o projeto e compartilhe com outros

## 📄 Licença

Este projeto está sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License - Copyright (c) 2025 Jesse Fernandes - ICTA Technology
```

## 👥 Equipe

### Desenvolvedor Principal
- **Jesse Fernandes** - [@jesseff20](https://github.com/jesseff20)
  - Email: jesse.fernandes@ictatechnology.com
  - LinkedIn: [Jesse Fernandes](https://linkedin.com/in/jesse-fernandes)

### ICTA Technology
- **Website**: [ictatechnology.com](https://ictatechnology.com)
- **Email**: contato@ictatechnology.com
- **Especialidades**: BI, Automação, IA, Integração de Sistemas

## 🙏 Agradecimentos

- **Hugging Face** - Pela plataforma e modelos
- **Facebook AI Research** - Pelo FAISS
- **Sentence Transformers** - Pelos modelos de embedding
- **Comunidade Python** - Pelas ferramentas e bibliotecas

---

## ⭐ Se este projeto foi útil, deixe uma estrela!

**[⭐ Star no GitHub](https://github.com/jesseff20/rag-chatbot)**

---

*Desenvolvido com ❤️ pela equipe ICTA Technology*

**Última atualização**: 29 de agosto de 2025

# 2) Abrir o chat (modo padrão: FLAN-T5 local)
python rag_chatbot_icta.py --chat \
    --index-path ./index/faiss.index \
    --meta-path ./index/meta.jsonl \
    --generator flan-t5 \
    --model-name google/flan-t5-base

# (Opcional) usar FLAN-T5-Large (maior, melhor qualidade)
python rag_chatbot_icta.py --chat --generator flan-t5 --model-name google/flan-t5-large

# (Opcional) usar endpoint TGI (Mistral 7B Instruct auto-hospedado)
#  - Suba um servidor TGI local (ex.: docker) com o modelo "mistralai/Mistral-7B-Instruct-v0.3"
#  - Depois, aponte a URL do servidor (ex.: http://localhost:8080)
python rag_chatbot_icta.py --chat \
    --generator tgi \
    --tgi-url http://localhost:8080 \
    --system-language pt

Observações importantes
----------------------
- Baixar os modelos pela primeira vez requer internet. Depois pode rodar offline.
- Em máquinas modestas, prefira flan-t5-base (mais leve). O Mistral 7B geralmente requer GPU + TGI.
- Não usar APIs pagas: aqui usamos modelos locais ou seu próprio endpoint TGI (gratuito para você).

Estrutura inicial para o chatbot RAG local:
- `data/` — arquivos `.txt` com FAQs e descrições de serviços.
- `index/` — será preenchida após rodar `--build-index` (FAISS + metadados).
- `history/` — arquivo `chat_history.jsonl` será criado durante o chat.

Passos rápidos:
1) Coloque seus `.txt` em `data/` (ou edite os exemplos incluídos).
2) Construa o índice:
   ```bash
   python rag_chatbot_icta.py --build-index --docs-path ./data --index-path ./index/faiss.index --meta-path ./index/meta.jsonl
   ```
3) Rode o chat:
   ```bash
   python rag_chatbot_icta.py --chat --index-path ./index/faiss.index --meta-path ./index/meta.jsonl --generator flan-t5 --model-name google/flan-t5-base
   ```

Observação: o script `rag_chatbot_icta.py` está disponível na conversa (canvas). Se preferir, salve-o na mesma pasta deste pacote.
