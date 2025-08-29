# Contribuindo para o RAG Chatbot ICTA

Obrigado pelo interesse em contribuir! Este documento explica como você pode ajudar a melhorar o projeto.

## Como Contribuir

### 1. Reportar Bugs
- Use o [GitHub Issues](https://github.com/jesseff20/rag-chatbot/issues)
- Descreva o problema claramente
- Inclua passos para reproduzir
- Informe versão do Python e sistema operacional

### 2. Sugerir Melhorias
- Use o [GitHub Issues](https://github.com/jesseff20/rag-chatbot/issues) com label "enhancement"
- Explique o benefício da melhoria
- Se possível, sugira uma implementação

### 3. Contribuir com Código

#### Setup do Ambiente de Desenvolvimento
```bash
# Clone o repositório
git clone https://github.com/jesseff20/rag-chatbot.git
cd rag-chatbot

# Instale em modo desenvolvimento
pip install -e ".[dev]"

# Execute os testes
python -m pytest test_rag_chatbot.py -v
```

#### Processo de Contribuição
1. **Fork** do repositório
2. **Crie uma branch** para sua feature: `git checkout -b feature/nova-funcionalidade`
3. **Faça suas mudanças** seguindo os padrões do projeto
4. **Execute os testes**: `python -m pytest`
5. **Execute o linting**: `flake8 *.py`
6. **Formate o código**: `black *.py`
7. **Commit suas mudanças**: `git commit -am 'Adiciona nova funcionalidade'`
8. **Push para sua branch**: `git push origin feature/nova-funcionalidade`
9. **Abra um Pull Request**

### 4. Padrões de Código

#### Python
- Use Python 3.8+
- Siga PEP 8
- Use type hints
- Docstrings para funções públicas
- Máximo 88 caracteres por linha (Black)

#### Commits
- Use mensagens claras e descritivas
- Prefira commits pequenos e focados
- Use português ou inglês consistentemente

#### Testes
- Adicione testes para novas funcionalidades
- Mantenha cobertura de testes alta
- Use pytest

## Estrutura do Projeto

```
rag-chatbot/
├── rag_chatbot_icta.py      # Módulo principal
├── requirements.txt         # Dependências
├── setup.py                # Configuração do pacote
├── test_rag_chatbot.py     # Testes
├── install.py              # Script de instalação
├── data/                   # Dados de exemplo
├── index/                  # Índices (gerados)
└── history/               # Histórico (gerado)
```

## Áreas que Precisam de Ajuda

- [ ] Melhorar interface do usuário
- [ ] Adicionar suporte a mais formatos de entrada (PDF, DOCX)
- [ ] Implementar cache inteligente
- [ ] Adicionar métricas de qualidade
- [ ] Melhorar documentação
- [ ] Adicionar mais testes
- [ ] Suporte a outros modelos de embedding
- [ ] Interface web opcional

## Recursos Úteis

- [Documentação FAISS](https://faiss.ai/)
- [Sentence Transformers](https://www.sbert.net/)
- [Transformers Hugging Face](https://huggingface.co/docs/transformers/)
- [Pytest Documentation](https://docs.pytest.org/)

## Dúvidas?

- Abra uma [Issue](https://github.com/jesseff20/rag-chatbot/issues)
- Entre em contato: jesse.fernandes@ictatechnology.com

Obrigado por contribuir! 🚀
