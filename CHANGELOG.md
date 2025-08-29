# Changelog - RAG Chatbot ICTA Technology

Todas as mudanças importantes deste projeto serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2025-08-29

### 🚀 Inovações Revolucionárias
- **Sistema Híbrido RAG + FLAN-T5**: Combina busca vetorial com geração de linguagem natural
- **Tokens Aumentados 6500%**: De 150 para 10,000 tokens por processamento
- **FLAN-T5 Base**: Upgrade para modelo mais robusto e preciso
- **Prompts Nativos em Português**: Otimizados especificamente para português brasileiro
- **Fallback Inteligente Múltiplo**: 4 camadas de segurança para sempre responder

### ✨ Adicionado
- Sistema híbrido que combina RAG + FLAN-T5 para respostas otimizadas
- Classe `PortugueseLLM` para processamento em português
- Função `generate_enhanced_answer_with_context()` para RAG + FLAN-T5
- Função `generate_enhanced_answer_without_context()` para FLAN-T5 puro
- Limpeza automática de tags técnicas [TAGS:] do contexto RAG
- Validação rigorosa de qualidade das respostas (15-400 caracteres)
- Sistema de scores para avaliar qualidade do contexto RAG (threshold 0.4)
- Carregamento robusto com fallback automático para modelos alternativos
- Interface silenciosa que oculta detalhes técnicos do usuário

### 🔧 Alterado
- **Chunk Size**: 400 → 600 tokens (+50% contexto)
- **Top-K Results**: 8 → 12 (+50% precisão na busca)
- **Max Tokens**: 150 → 10,000 (+6,567% capacidade)
- **Overlap**: 80 → 120 tokens (+50% continuidade)
- **FLAN-T5 Tokens**: 150 → 300 (+100% saída)
- **Modelo Principal**: google/flan-t5-base (mais estável que GPT-2)
- **Prompts Otimizados**: Estruturados para português com contexto claro
- **Contexto RAG**: Limitado a 2 linhas mais relevantes

### 🐛 Corrigido
- Respostas muito longas e desconexas do GPT-2 português
- Loops infinitos em respostas inadequadas
- Travamentos com contextos muito longos
- Inconsistências na interface multilíngue
- Problemas de memória com modelos grandes
- Warnings do transformers sobre beam search

### 🗑️ Removido
- Dependência problemática do pierreguillou/gpt2-small-portuguese
- Parâmetros early_stopping e length_penalty que causavam warnings
- Exposição de scores e informações técnicas na interface

## [3.0.0] - 2025-08-28

### ✨ Adicionado
- Interface totalmente interativa com menus coloridos
- Sistema de ajuda integrado dentro do programa
- Verificação de status em tempo real
- Detecção automática de problemas com sugestões
- Análise de intenção automática com FLAN-T5
- Sistema de feedback inteligente
- Histórico de conversas com timestamp

### 🔧 Alterado
- Substituição completa da interface de linha de comando
- Menus coloridos e intuitivos
- Explicações detalhadas em cada opção
- Performance de processamento melhorada

### 🐛 Corrigido
- Problemas com encoding de caracteres especiais
- Erros de path no Windows
- Travamentos durante processamento
- Mensagens de erro confusas

## [2.0.0] - 2025-08-27

### ✨ Adicionado
- Sistema RAG (Retrieval-Augmented Generation) completo
- Suporte a arquivos .txt e .jsonl
- Busca vetorial com FAISS
- Embeddings multilíngues com Sentence Transformers
- Modelo FLAN-T5 para geração de respostas
- Sistema de chunks com overlap
- Interface de linha de comando interativa

### 🔧 Alterado
- Arquitetura completamente reescrita
- Foco em português brasileiro
- Otimizações de performance

### 🐛 Corrigido
- Problemas de compatibilidade entre sistemas
- Erros de dependências
- Questões de encoding

## [1.0.0] - 2025-08-26

### ✨ Adicionado
- Versão inicial do chatbot
- Funcionalidades básicas de FAQ
- Estrutura de projeto inicial
- Documentação básica

---

## Tipos de Mudanças

- **🚀 Inovações Revolucionárias**: Mudanças que transformam completamente o sistema
- **✨ Adicionado**: Para novas funcionalidades
- **🔧 Alterado**: Para mudanças em funcionalidades existentes
- **🐛 Corrigido**: Para correções de bugs
- **🗑️ Removido**: Para funcionalidades removidas
- **🔒 Segurança**: Para vulnerabilidades corrigidas
