# 🤝 Como Contribuir - RAG Chatbot ICTA Technology

Ficamos felizes que você queira contribuir! Este documento explica como fazer isso de forma eficiente.

> 📍 **Versão 2.0**: Agora com interface simplificada! Contribuições para tornar ainda mais fácil são bem-vindas.

## 🎯 Tipos de Contribuição

### 🐛 **Reportar Bugs**
- Use o [GitHub Issues](https://github.com/jesseff20/rag-chatbot/issues)
- Escolha template "Bug Report"
- Inclua screenshots se possível
- Descreva passos para reproduzir

### 💡 **Sugerir Melhorias**
- Use o [GitHub Discussions](https://github.com/jesseff20/rag-chatbot/discussions)
- Explique o caso de uso
- Proponha solução se possível

### 📖 **Melhorar Documentação**
- Corrija erros de escrita
- Adicione exemplos práticos
- Melhore explicações técnicas
- Traduza para outros idiomas

### 🔧 **Contribuir com Código**
- Novas funcionalidades
- Correções de bugs
- Melhorias de performance
- Refatoração de código

## 🚀 Setup do Ambiente de Desenvolvimento

### 📦 **1. Fork e Clone**
```bash
# 1. Faça fork no GitHub
# 2. Clone seu fork
git clone https://github.com/SEU_USER/rag-chatbot.git
cd rag-chatbot

# 3. Adicione o repositório original
git remote add upstream https://github.com/jesseff20/rag-chatbot.git
```

### 🐍 **2. Configurar Python**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar dependências de desenvolvimento
pip install -e ".[dev]"
```

### 🧪 **3. Executar Testes**
```bash
# Executar todos os testes
python -m pytest tests/ -v

# Testes com coverage
python -m pytest tests/ --cov=rag_chatbot_icta --cov-report=html

# Linting
flake8 rag_chatbot_icta.py
black --check rag_chatbot_icta.py
```

## 📝 Padrões de Código

### 🎨 **Formatação**
- **Python**: Siga PEP 8
- **Imports**: Use isort
- **Formatação**: Use black
- **Docstrings**: Formato Google style

### 🏗️ **Estrutura**
```python
def funcao_exemplo(param: str) -> dict[str, Any]:
    """Descrição breve da função.
    
    Args:
        param: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
        
    Raises:
        ValueError: Quando param é inválido
    """
    # Implementação
    pass
```

### 🎯 **Nomenclatura**
- **Funções**: snake_case
- **Classes**: PascalCase
- **Constantes**: UPPER_CASE
- **Variáveis**: snake_case descritivas

## 🔄 Fluxo de Contribuição

### 📋 **1. Planejamento**
```bash
# Sincronizar com upstream
git fetch upstream
git checkout main
git merge upstream/main

# Criar branch para feature
git checkout -b feature/nova-funcionalidade
```

### 💻 **2. Desenvolvimento**
```bash
# Fazer alterações
# Escrever testes
# Executar testes

# Commits atômicos
git add .
git commit -m "feat: adiciona nova funcionalidade"
```

### 🧪 **3. Testes e Qualidade**
```bash
# Executar suite completa
python -m pytest tests/

# Verificar formatação
black rag_chatbot_icta.py
flake8 rag_chatbot_icta.py

# Testar interface interativa
python rag_chatbot_icta.py
```

### 📤 **4. Pull Request**
```bash
# Push da branch
git push origin feature/nova-funcionalidade

# Criar PR no GitHub
# Aguardar review
# Fazer ajustes se necessário
```

## 🏷️ Convenções de Commit

### 📋 **Formato**
```
tipo(escopo): descrição breve

Descrição mais detalhada se necessário.

Closes #123
```

### 🎯 **Tipos**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas administrativas

### 💡 **Exemplos**
```bash
feat(chat): adiciona comando help no chat interativo
fix(build): corrige erro de encoding em arquivos Windows
docs(readme): atualiza guia de instalação
style(menu): melhora cores e formatação dos menus
```

## 🎨 Guia de Interface

### 🌈 **Cores (Colorama)**
```python
# Sucesso e confirmações
Fore.GREEN

# Informações e processamento
Fore.BLUE, Fore.CYAN

# Alertas e dicas
Fore.YELLOW

# Erros
Fore.RED

# Texto secundário
Fore.LIGHTBLACK_EX
```

### 📱 **Design de Menus**
```python
def print_menu_option(number: int, title: str, description: str):
    """Padrão para opções de menu"""
    print(f"{Fore.YELLOW}{number:2}. {Fore.WHITE}{title}")
    print(f"    {Fore.LIGHTBLACK_EX}{description}{Style.RESET_ALL}")
```

### 💬 **Mensagens de Usuário**
- ✅ Use emojis para clareza visual
- 🎯 Seja direto e claro
- 💡 Ofereça dicas quando possível
- 🆘 Sempre sugira próximos passos

## 🧪 Testes

### 📋 **O que Testar**
- Funcionalidade core (build, chat, search)
- Interface do usuário (menus, validação)
- Tratamento de erros
- Casos extremos

### 🔧 **Como Escrever Testes**
```python
def test_build_knowledge_base():
    """Testa construção da base de conhecimento"""
    # Arrange
    docs = {"test.txt": "P: teste R: resposta"}
    
    # Act
    result = build_knowledge_base(docs)
    
    # Assert
    assert result.success
    assert result.total_chunks > 0
```

### 🎯 **Cobertura**
- Mantenha cobertura > 80%
- Foque nos casos críticos
- Teste happy path e edge cases

## 📖 Documentação

### 📝 **README.md**
- Mantenha atualizado com novas features
- Use exemplos práticos
- Screenshots da interface ajudam

### 📚 **Código**
- Docstrings em todas as funções públicas
- Comentários para lógica complexa
- Type hints sempre que possível

### 🎯 **Ajuda Integrada**
- Mantenha help text atualizado
- Exemplos práticos
- Solução de problemas comuns

## 🚀 Review Process

### 👀 **O que Reviewamos**
- Funcionalidade correta
- Testes adequados
- Documentação atualizada
- Interface user-friendly
- Performance adequada

### ⏱️ **Timeline**
- Reviews iniciais: 2-3 dias
- Feedback e ajustes: iterativo
- Merge: após aprovação

### 💡 **Dicas para Aprovação Rápida**
- PRs pequenos e focados
- Testes completos
- Documentação clara
- Interface consistente

## 🎯 Áreas que Precisam de Ajuda

### 🔥 **Alta Prioridade**
- Melhorias na interface interativa
- Mais opções de configuração visual
- Sistema de plugins/extensões
- Suporte a mais formatos de arquivo

### 🌟 **Desejável**
- Interface web opcional
- Métricas de qualidade das respostas
- Integração com mais modelos
- Documentação em vídeo

### 🧪 **Experimental**
- Suporte a imagens
- Integração com APIs externas
- Deploy automatizado
- CI/CD melhorado

## 📞 Suporte para Contribuidores

### 💬 **Canais de Comunicação**
- **GitHub Discussions**: Para dúvidas gerais
- **GitHub Issues**: Para bugs específicos
- **Email**: jesse.fernandes@ictatechnology.com
- **Pull Requests**: Para feedback técnico

### 🆘 **Precisa de Ajuda?**
1. Veja issues marcadas como "good first issue"
2. Leia a documentação completa
3. Execute o programa e teste a interface
4. Não hesite em perguntar!

## 🏆 Reconhecimento

### 📋 **Contributors**
Todos os contribuidores serão listados no:
- README.md
- Arquivo CONTRIBUTORS.md
- Release notes
- GitHub contributors page

### 🎉 **Tipos de Reconhecimento**
- **Code**: Commits e PRs
- **Documentation**: Melhorias na docs
- **Design**: Interface e UX
- **Testing**: Testes e QA
- **Ideas**: Sugestões implementadas

---

## 💝 Obrigado!

Cada contribuição, por menor que seja, faz diferença! Juntos estamos tornando a IA mais acessível para todos.

**🌟 Não se esqueça de dar uma estrela no projeto se ele te ajudou!**
