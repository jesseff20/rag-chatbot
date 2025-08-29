#!/usr/bin/env python3
"""
RAG Chatbot ICTA Technology - Versão Simplificada com Menus Interativos
Sistema amigável para criação de chatbot FAQ

Autor: Jesse Fernandes - ICTA Technology
GitHub: https://github.com/jesseff20/rag-chatbot
"""

from __future__ import annotations
import os
import json
import sys
import time
from datetime import datetime
from dataclasses import dataclass
from typing import Any, List, Dict, Optional

# Imports principais
import faiss  # type: ignore
import numpy as np
from tqdm import tqdm
from colorama import Fore, Style, init, Back
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Inicializar colorama para Windows
init(autoreset=True)

# ================================
# Configurações Padrão
# ================================

DEFAULT_CONFIG = {
    "docs_path": "./data",
    "index_path": "./index/faiss.index",
    "meta_path": "./index/meta.jsonl",
    "settings_path": "./index/settings.json",
    "history_path": "./history/chat_history.jsonl",
    "chunk_size": 600,  # Aumentado para chunks maiores
    "overlap": 120,     # Sobreposição otimizada (20% do chunk_size)
    "top_k": 12,        # Aumentado para recuperar mais contexto relevante
    "max_tokens": 10000,  # Significativamente aumentado para respostas mais completas
    "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",  # Melhor para português
    "generation_model": "google/flan-t5-base",  # Volta para FLAN-T5 que é mais estável
    "fallback_model": "google/flan-t5-small"  # Fallback menor
}

# ================================
# Classes de Dados
# ================================

@dataclass
class Metadata:
    source: str
    chunk_id: int
    start_char: int
    end_char: int

@dataclass  
class Retrieved:
    text: str
    meta: Metadata
    score: float

# ================================
# Sistema Híbrido RAG + FLAN-T5
# ================================

class FlanT5Fallback:
    """Sistema de fallback usando FLAN-T5 quando RAG não tem resposta adequada"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Carrega o modelo FLAN-T5 para fallback"""
        if self.is_loaded:
            return True
            
        try:
            print(f"{Fore.BLUE}🤖 Carregando modelo FLAN-T5 para respostas de fallback...")
            
            # Usar modelo do config
            model_name = DEFAULT_CONFIG["generation_model"]
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Mover para GPU se disponível
            if torch.cuda.is_available():
                self.model = self.model.to(self.device)
                print(f"  🚀 Modelo carregado na GPU")
            else:
                print(f"  💻 Modelo carregado na CPU")
                
            self.is_loaded = True
            print(f"{Fore.GREEN}✅ FLAN-T5 pronto para fallback!")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Erro ao carregar FLAN-T5: {e}")
            return False
    
    def generate_fallback_response(self, question: str, context_type: str = "") -> str:
        """Gera resposta usando FLAN-T5 quando RAG não tem resposta"""
        if not self.is_loaded:
            if not self.load_model():
                return "Desculpe, não consegui processar sua pergunta no momento. Tente novamente mais tarde."
        
        try:
            # Criar prompt contextualizado para ICTA
            icta_context = """A ICTA Technology é uma consultoria especializada em:
• Business Intelligence (BI) e Analytics
• Automação de processos e RPA
• Inteligência Artificial e Machine Learning
• Integrações com sistemas ERP (especialmente TOTVS)
• Transformação digital e otimização de dados

Principais serviços:
- Dashboards e relatórios executivos
- Automação de workflows
- Chatbots e assistentes virtuais
- Migração e integração de dados
- Consultoria em arquitetura de dados"""

            prompt = f"""Você é um assistente especializado da ICTA Technology. Responda de forma útil e profissional.

CONTEXTO DA EMPRESA:
{icta_context}

PERGUNTA DO CLIENTE: {question}

INSTRUÇÕES:
- Seja profissional e útil
- Use informações gerais sobre tecnologia quando apropriado
- Se não souber algo específico da ICTA, seja honesto
- Sugira entrar em contato para informações detalhadas
- Mantenha foco em BI, automação, IA e integrações

RESPOSTA:"""

            # Tokenizar e gerar resposta
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                max_length=600, 
                truncation=True
            )
            
            # Mover inputs para dispositivo correto
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=800,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Limpar resposta (remover prompt repetido)
            response = response.replace(prompt, "").strip()
            
            # Adicionar disclaimer sobre ser resposta geral
            disclaimer = "\n\n💡 *Resposta gerada por IA geral. Para informações específicas da ICTA, entre em contato conosco.*"
            
            return response + disclaimer
            
        except Exception as e:
            print(f"{Fore.RED}❌ Erro ao gerar resposta com FLAN-T5: {e}")
            return f"Desculpe, tive um problema técnico. Para melhor atendimento, entre em contato diretamente com nossa equipe da ICTA Technology."

# Instância global do sistema de fallback
flan_fallback = FlanT5Fallback()

class PortugueseLLM:
    """FLAN-T5 otimizado para português com prompts melhorados"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_model(self) -> bool:
        """Carrega o modelo FLAN-T5 otimizado para português"""
        try:
            model_name = DEFAULT_CONFIG["generation_model"]
            print(f"🤖 Carregando FLAN-T5 otimizado: {model_name}")
            
            # Usar FLAN-T5 que é mais estável
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Configurar padding token se não existir
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Mover para dispositivo apropriado
            if self.device == "cuda" and torch.cuda.is_available():
                try:
                    self.model = self.model.to(self.device)
                    print(f"  🚀 Modelo carregado na GPU")
                except:
                    self.device = "cpu"
                    print(f"  💻 Modelo carregado na CPU (GPU não disponível)")
            else:
                print(f"  💻 Modelo carregado na CPU")
            
            self.is_loaded = True
            print("✅ FLAN-T5 otimizado carregado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar FLAN-T5: {e}")
            self.is_loaded = False
            return False
    
    def generate_enhanced_response(self, question: str, rag_context: str = "") -> str:
        """Gera resposta usando FLAN-T5 com prompts otimizados para português"""
        try:
            if not self.is_loaded:
                success = self.load_model()
                if not success:
                    return "Erro ao carregar modelo. Tente novamente."
            
            # Criar prompt otimizado para FLAN-T5 em português
            if rag_context:
                # Limitar e limpar contexto RAG
                context_lines = rag_context.split('\n')[:2]  # Usar apenas 2 linhas
                clean_context = ' '.join(context_lines).strip()
                clean_context = clean_context.replace('[TAGS:', '').replace(']', '')
                
                prompt = f"""Baseado nas informações da ICTA Technology, responda de forma clara e profissional em português.

Informações: {clean_context}

Pergunta: {question}

Resposta clara em português:"""
            else:
                # Prompt para perguntas gerais
                prompt = f"""Responda como assistente profissional da ICTA Technology em português.

A ICTA Technology é especializada em Business Intelligence, automação de processos e inteligência artificial para empresas.

Pergunta: {question}

Resposta profissional:"""
            
            # Tokenizar com limite adequado
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=400,
                truncation=True,
                padding=True
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Gerar resposta com parâmetros otimizados para FLAN-T5
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=100,  # Quantidade adequada para FLAN-T5
                    temperature=0.3,     # Conservador para informações específicas
                    do_sample=True,
                    top_p=0.8,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            # Decodificar resposta
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extrair apenas a resposta nova
            if "Resposta clara em português:" in response:
                response = response.split("Resposta clara em português:")[-1].strip()
            elif "Resposta profissional:" in response:
                response = response.split("Resposta profissional:")[-1].strip()
            else:
                # Remover o prompt original
                response = response.replace(prompt, "").strip()
            
            # Limpeza e validação final
            if len(response) < 15 or len(response) > 400:
                if rag_context:
                    # Usar resposta direta do RAG se disponível
                    return clean_context if clean_context else "Entre em contato para mais informações sobre os serviços da ICTA Technology."
                else:
                    return "A ICTA Technology oferece soluções em Business Intelligence, automação e inteligência artificial. Entre em contato para mais informações."
            
            return response
            
        except Exception as e:
            print(f"Erro no modelo FLAN-T5: {e}")
            if rag_context:
                # Fallback para contexto RAG direto
                clean_context = rag_context.replace('[TAGS:', '').replace(']', '').strip()
                return clean_context.split('\n')[0] if clean_context else "Entre em contato para mais informações."
            return "Para informações específicas, entre em contato com a ICTA Technology."

# Instância global do modelo português
portuguese_llm = PortugueseLLM()

# ================================
# Utilitários de Interface
# ================================

def print_header():
    """Imprime cabeçalho do programa"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🤖 RAG Chatbot ICTA Technology - Versão Simplificada")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.GREEN}Sistema interativo para criação de chatbot FAQ")
    print(f"{Fore.GREEN}GitHub: https://github.com/jesseff20/rag-chatbot")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_menu_option(number: int, title: str, description: str):
    """Imprime uma opção do menu formatada"""
    print(f"{Fore.YELLOW}{number:2}. {Fore.WHITE}{title}")
    print(f"    {Fore.LIGHTBLACK_EX}{description}{Style.RESET_ALL}")

def get_user_choice(max_option: int) -> int:
    """Obtém escolha do usuário com validação"""
    while True:
        try:
            choice = input(f"\n{Fore.CYAN}🎯 Escolha uma opção (1-{max_option}): {Style.RESET_ALL}")
            choice_num = int(choice)
            if 1 <= choice_num <= max_option:
                return choice_num
            else:
                print(f"{Fore.RED}❌ Por favor, escolha um número entre 1 e {max_option}")
        except ValueError:
            print(f"{Fore.RED}❌ Por favor, digite um número válido")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Saindo do programa...")
            sys.exit(0)

def confirm_action(message: str) -> bool:
    """Confirma uma ação com o usuário"""
    while True:
        response = input(f"{Fore.YELLOW}❓ {message} (s/n): {Style.RESET_ALL}").lower().strip()
        if response in ['s', 'sim', 'y', 'yes']:
            return True
        elif response in ['n', 'nao', 'não', 'no']:
            return False
        else:
            print(f"{Fore.RED}❌ Digite 's' para sim ou 'n' para não")

def wait_for_enter():
    """Espera o usuário pressionar Enter"""
    _ = input(f"\n{Fore.LIGHTBLACK_EX}📝 Pressione Enter para continuar...{Style.RESET_ALL}")

# ================================
# Utilitários de Processamento
# ================================

def read_jsonl_files(folder: str) -> dict[str, str]:
    """Lê todos os .jsonl do diretório com processamento inteligente"""
    print(f"{Fore.BLUE}📂 Lendo arquivos .jsonl de: {folder}")
    
    if not os.path.exists(folder):
        print(f"{Fore.RED}❌ Diretório não encontrado: {folder}")
        return {}
    
    data: dict[str, str] = {}
    jsonl_files = []
    
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".jsonl"):
                jsonl_files.append(os.path.join(root, f))
    
    if not jsonl_files:
        print(f"{Fore.YELLOW}⚠️ Nenhum arquivo .jsonl encontrado em {folder}")
        return {}
    
    print(f"{Fore.GREEN}📄 Encontrados {len(jsonl_files)} arquivos .jsonl")
    
    for fp in tqdm(jsonl_files, desc="Lendo arquivos"):
        try:
            content_parts = []
            with open(fp, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        entry = json.loads(line)
                        # Processa e enriquece cada entrada
                        processed_entry = process_jsonl_entry(entry, os.path.basename(fp))
                        if processed_entry:
                            content_parts.append(processed_entry)
                        
            if content_parts:
                content = "\n\n".join(content_parts)
                data[fp] = content
                print(f"{Fore.GREEN}  ✅ {os.path.basename(fp)} ({len(content_parts)} entradas, {len(content)} caracteres)")
            else:
                print(f"{Fore.YELLOW}  ⚠️ {os.path.basename(fp)} está vazio")
        except Exception as e:
            print(f"{Fore.RED}  ❌ Erro ao ler {os.path.basename(fp)}: {e}")
    
    return data

def process_jsonl_entry(entry: dict, filename: str) -> str:
    """Processa uma entrada JSONL para enriquecer o contexto"""
    
    # Determina o contexto baseado no nome do arquivo
    context_prefix = ""
    if "cortesia" in filename.lower() or "saudacao" in filename.lower():
        context_prefix = "[SAUDAÇÃO/CORTESIA] "
    elif "empresa" in filename.lower() or "contato" in filename.lower():
        context_prefix = "[EMPRESA/CONTATO] "
    elif "faq" in filename.lower():
        context_prefix = "[FAQ GERAL] "
    elif "servicos" in filename.lower() or "bi" in filename.lower() or "automacao" in filename.lower():
        context_prefix = "[SERVIÇOS/BI/AUTOMAÇÃO] "
    elif "integracao" in filename.lower() or "totvs" in filename.lower():
        context_prefix = "[INTEGRAÇÃO/TOTVS] "
    elif "politica" in filename.lower():
        context_prefix = "[POLÍTICA/DIRETRIZES] "
    
    # Processa diferentes estruturas de entrada
    processed_text = ""
    
    if 'question' in entry and 'answer' in entry:
        # Formato completo com pergunta e resposta
        processed_text = f"PERGUNTA: {entry['question']}\nRESPOSTA: {entry['answer']}"
    elif 'answer' in entry:
        # Apenas resposta - tenta inferir o contexto
        answer = entry['answer'].strip()
        
        # Adiciona contexto semântico baseado no conteúdo
        if any(word in answer.lower() for word in ['bom dia', 'boa tarde', 'boa noite', 'olá', 'oi']):
            context_prefix = "[SAUDAÇÃO] "
        elif any(word in answer.lower() for word in ['preço', 'custo', 'investimento', 'valor']):
            context_prefix = "[PREÇOS/COMERCIAL] "
        elif any(word in answer.lower() for word in ['totvs', 'erp', 'integração']):
            context_prefix = "[INTEGRAÇÃO/ERP] "
        elif any(word in answer.lower() for word in ['bi', 'business intelligence', 'dashboard', 'relatório']):
            context_prefix = "[BUSINESS INTELLIGENCE] "
        elif any(word in answer.lower() for word in ['automação', 'rpa', 'processo']):
            context_prefix = "[AUTOMAÇÃO] "
        elif any(word in answer.lower() for word in ['ia', 'inteligência artificial', 'chatbot', 'ai']):
            context_prefix = "[INTELIGÊNCIA ARTIFICIAL] "
        elif any(word in answer.lower() for word in ['contato', 'telefone', 'email', 'endereço']):
            context_prefix = "[CONTATO/LOCALIZAÇÃO] "
        
        processed_text = f"CONTEÚDO: {answer}"
    elif 'text' in entry:
        processed_text = f"TEXTO: {entry['text']}"
    elif isinstance(entry, str):
        processed_text = f"INFORMAÇÃO: {entry}"
    else:
        return ""
    
    # Adiciona metadados para melhor recuperação
    enhanced_text = f"{context_prefix}{processed_text}"
    
    # Adiciona palavras-chave relevantes para ICTA
    keywords = []
    text_lower = processed_text.lower()
    
    # Palavras-chave técnicas
    if any(word in text_lower for word in ['dashboard', 'relatório', 'análise', 'dados']):
        keywords.append("business_intelligence")
    if any(word in text_lower for word in ['automação', 'automatizar', 'processo']):
        keywords.append("automacao_processos")
    if any(word in text_lower for word in ['totvs', 'erp', 'protheus']):
        keywords.append("integracao_erp")
    if any(word in text_lower for word in ['chatbot', 'ia', 'inteligência']):
        keywords.append("inteligencia_artificial")
    if any(word in text_lower for word in ['python', 'sql', 'api']):
        keywords.append("tecnologia")
    
    if keywords:
        enhanced_text += f" [TAGS: {', '.join(keywords)}]"
    
    return enhanced_text

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80) -> list[str]:
    """Quebra texto em chunks inteligentes com sobreposição otimizada"""
    import re
    
    chunks = []
    
    # Primeiro, tenta quebrar por sentenças completas
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if not sentences:
        sentences = [text]
    
    current_chunk = ""
    
    for sentence in sentences:
        # Se adicionar a próxima sentença não exceder o limite
        if len(current_chunk + " " + sentence) <= chunk_size:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
        else:
            # Se o chunk atual não está vazio, salva
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            # Se a sentença é muito longa, quebra por caracteres
            if len(sentence) > chunk_size:
                # Quebra a sentença longa mantendo palavras inteiras
                words = sentence.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk + " " + word) <= chunk_size:
                        if temp_chunk:
                            temp_chunk += " " + word
                        else:
                            temp_chunk = word
                    else:
                        if temp_chunk.strip():
                            chunks.append(temp_chunk.strip())
                        temp_chunk = word
                
                current_chunk = temp_chunk
            else:
                current_chunk = sentence
    
    # Adiciona o último chunk se não estiver vazio
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # Se ainda não temos chunks, faz quebra simples por caracteres
    if not chunks and text.strip():
        start = 0
        n = len(text)
        while start < n:
            end = min(start + chunk_size, n)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end == n:
                break
            start = end - overlap
            if start < 0:
                start = 0
    
    # Adiciona sobreposição inteligente entre chunks adjacentes
    enhanced_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            enhanced_chunks.append(chunk)
        else:
            # Adiciona sobreposição com o chunk anterior
            prev_chunk = chunks[i-1]
            overlap_text = prev_chunk[-overlap:] if len(prev_chunk) > overlap else prev_chunk
            
            # Remove pontuação quebrada no início da sobreposição
            overlap_text = re.sub(r'^[^\w\s]*', '', overlap_text)
            
            if overlap_text.strip() and not chunk.startswith(overlap_text.strip()):
                enhanced_chunk = overlap_text.strip() + " " + chunk
            else:
                enhanced_chunk = chunk
            
            enhanced_chunks.append(enhanced_chunk)
    
    return enhanced_chunks

# ================================
# Menu Principal
# ================================

def show_main_menu():
    """Exibe o menu principal"""
    print(f"\n{Fore.CYAN}📋 MENU PRINCIPAL")
    print(f"{Fore.CYAN}{'='*50}")
    
    print_menu_option(1, "🏗️ Construir Base de Conhecimento", 
                     "Processa seus arquivos .jsonl e cria o índice de busca")
    
    print_menu_option(2, "💬 Chat Interativo Inteligente", 
                     "Conversa inteligente com IA que guia quando necessário")
    
    print_menu_option(3, "📊 Verificar Status do Sistema", 
                     "Mostra informações sobre arquivos e configurações")
    
    print_menu_option(4, "⚙️ Configurações", 
                     "Ajustar parâmetros básicos do sistema")
    
    print_menu_option(5, "📚 Ajuda", 
                     "Guias, exemplos e solução de problemas")
    
    print_menu_option(6, "🚪 Sair", 
                     "Encerra o programa")

# ================================
# Sistema de Status
# ================================

def check_system_status():
    """Verifica e mostra status do sistema"""
    print(f"\n{Fore.GREEN}📊 STATUS DO SISTEMA")
    print(f"{Fore.GREEN}{'='*40}")
    
    config = DEFAULT_CONFIG
    
    # Verificar diretórios
    print(f"\n{Fore.CYAN}📁 Diretórios:")
    dirs_to_check = [
        ("Data (documentos)", config["docs_path"]),
        ("Index (índices)", os.path.dirname(config["index_path"])),
        ("History (histórico)", os.path.dirname(config["history_path"]))
    ]
    
    for name, path in dirs_to_check:
        if os.path.exists(path):
            print(f"  ✅ {name}: {path}")
        else:
            print(f"  ❌ {name}: {path} (não encontrado)")
    
    # Verificar arquivos de dados
    print(f"\n{Fore.CYAN}📄 Arquivos de dados:")
    if os.path.exists(config["docs_path"]):
        jsonl_files = [f for f in os.listdir(config["docs_path"]) if f.endswith('.jsonl')]
        if jsonl_files:
            print(f"  ✅ {len(jsonl_files)} arquivos .jsonl encontrados:")
            for f in jsonl_files[:5]:  # Mostrar apenas os primeiros 5
                print(f"    📝 {f}")
            if len(jsonl_files) > 5:
                print(f"    ... e mais {len(jsonl_files) - 5} arquivos")
        else:
            print(f"  ⚠️ Nenhum arquivo .jsonl encontrado em {config['docs_path']}")
    else:
        print(f"  ❌ Diretório {config['docs_path']} não existe")
    
    # Verificar índice
    print(f"\n{Fore.CYAN}🔍 Índice de busca:")
    if os.path.exists(config["index_path"]):
        print(f"  ✅ Índice FAISS: {config['index_path']}")
        try:
            index = faiss.read_index(config["index_path"])
            print(f"  📊 Vetores no índice: {index.ntotal}")
        except Exception as e:
            print(f"  ⚠️ Erro ao ler índice: {e}")
    else:
        print(f"  ❌ Índice não encontrado: {config['index_path']}")
    
    if os.path.exists(config["meta_path"]):
        print(f"  ✅ Metadados: {config['meta_path']}")
        try:
            with open(config["meta_path"], 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            print(f"  📊 Chunks de texto: {lines}")
        except Exception as e:
            print(f"  ⚠️ Erro ao ler metadados: {e}")
    else:
        print(f"  ❌ Metadados não encontrados: {config['meta_path']}")
    
    # Verificar configurações
    print(f"\n{Fore.CYAN}⚙️ Configurações:")
    if os.path.exists(config["settings_path"]):
        print(f"  ✅ Arquivo de configurações existe")
        try:
            with open(config["settings_path"], 'r', encoding='utf-8') as f:
                settings = json.load(f)
            print(f"  📊 Modelo de embeddings: {settings.get('embedding_model', 'N/A')}")
            print(f"  📊 Dimensão: {settings.get('dimension', 'N/A')}")
            print(f"  📊 Criado em: {settings.get('created_at', 'N/A')}")
        except Exception as e:
            print(f"  ⚠️ Erro ao ler configurações: {e}")
    else:
        print(f"  ⚠️ Usando configurações padrão")
    
    # Recomendações
    print(f"\n{Fore.YELLOW}💡 Recomendações:")
    if not os.path.exists(config["docs_path"]):
        print("  • Crie o diretório 'data' e adicione arquivos .jsonl")
    elif not os.path.exists(config["index_path"]):
        print("  • Execute 'Construir Base de Conhecimento' (opção 1)")
    else:
        print("  • Sistema pronto! Use 'Iniciar Chat' (opção 2)")
    
    wait_for_enter()

# ================================
# Construção de Base de Conhecimento
# ================================

def build_knowledge_base():
    """Constrói a base de conhecimento de forma interativa"""
    print(f"\n{Fore.GREEN}🏗️ CONSTRUINDO BASE DE CONHECIMENTO")
    print(f"{Fore.GREEN}{'='*50}")
    
    config = DEFAULT_CONFIG.copy()
    
    # Verificar se já existe uma base de conhecimento
    base_exists = (os.path.exists(config["index_path"]) and 
                   os.path.exists(config["meta_path"]) and 
                   os.path.exists(config["settings_path"]))
    
    if base_exists:
        print(f"\n{Fore.YELLOW}⚠️ BASE DE CONHECIMENTO JÁ EXISTE!")
        print(f"{Fore.CYAN}📊 Arquivos encontrados:")
        print(f"  ✅ Índice FAISS: {config['index_path']}")
        print(f"  ✅ Metadados: {config['meta_path']}")
        print(f"  ✅ Configurações: {config['settings_path']}")
        
        # Mostrar informações da base atual
        try:
            with open(config["settings_path"], "r", encoding="utf-8") as f:
                settings = json.load(f)
            print(f"\n{Fore.CYAN}📋 Informações da base atual:")
            print(f"  📄 Total de documentos: {settings.get('total_documents', 'N/A')}")
            print(f"  📝 Total de chunks: {settings.get('total_chunks', 'N/A')}")
            print(f"  📅 Criado em: {settings.get('created_at', 'N/A')}")
            print(f"  🧠 Modelo: {settings.get('embedding_model', 'N/A')}")
        except Exception as e:
            print(f"{Fore.RED}❌ Erro ao ler configurações: {e}")
        
        print(f"\n{Fore.YELLOW}🔄 OPÇÕES DISPONÍVEIS:")
        print(f"  1️⃣ Reconstruir base (substituir atual)")
        print(f"  2️⃣ Manter base atual (cancelar)")
        
        rebuild_choice = get_user_choice(2)
        
        if rebuild_choice == 2:
            print(f"\n{Fore.GREEN}✅ Operação cancelada. Base atual mantida.")
            wait_for_enter()
            return
        
        print(f"\n{Fore.YELLOW}🗑️ Removendo base antiga...")
        try:
            if os.path.exists(config["index_path"]):
                os.remove(config["index_path"])
                print(f"  ✅ Índice removido")
            if os.path.exists(config["meta_path"]):
                os.remove(config["meta_path"])
                print(f"  ✅ Metadados removidos")
            if os.path.exists(config["settings_path"]):
                os.remove(config["settings_path"])
                print(f"  ✅ Configurações removidas")
        except Exception as e:
            print(f"{Fore.RED}❌ Erro ao remover arquivos: {e}")
            wait_for_enter()
            return
        
        print(f"{Fore.GREEN}✅ Base anterior removida com sucesso!")
        print(f"\n{Fore.GREEN}🏗️ RECONSTRUINDO BASE DE CONHECIMENTO...")
    
    # Verificar se diretório data existe
    if not os.path.exists(config["docs_path"]):
        print(f"{Fore.RED}❌ Diretório 'data' não encontrado!")
        if confirm_action("Deseja criar o diretório 'data'?"):
            os.makedirs(config["docs_path"], exist_ok=True)
            print(f"{Fore.GREEN}✅ Diretório 'data' criado!")
            print(f"{Fore.YELLOW}💡 Adicione seus arquivos .jsonl em '{config['docs_path']}' e tente novamente")
            wait_for_enter()
            return
        else:
            return
    
    # Ler arquivos
    documents = read_jsonl_files(config["docs_path"])
    if not documents:
        print(f"{Fore.RED}❌ Nenhum arquivo .jsonl encontrado ou todos estão vazios!")
        print(f"{Fore.YELLOW}💡 Adicione arquivos .jsonl em '{config['docs_path']}' e tente novamente")
        wait_for_enter()
        return
    
    print(f"\n{Fore.CYAN}📊 RESUMO DOS ARQUIVOS:")
    total_chars = 0
    for filepath, content in documents.items():
        filename = os.path.basename(filepath)
        char_count = len(content)
        total_chars += char_count
        print(f"  📄 {filename}: {char_count:,} caracteres")
    
    print(f"\n{Fore.GREEN}✅ Total: {len(documents)} arquivos, {total_chars:,} caracteres")
    
    if not confirm_action("Continuar com a construção do índice?"):
        return
    
    try:
        # Criar chunks com estratégia otimizada
        print(f"\n{Fore.BLUE}📝 Dividindo textos em chunks inteligentes...")
        chunks: list[str] = []
        metadatas: list[Metadata] = []
        
        total_content_chars = sum(len(content) for content in documents.values())
        print(f"  � Processando {total_content_chars:,} caracteres total")
        
        for filepath, content in documents.items():
            filename = os.path.basename(filepath)
            print(f"  📝 Processando {filename}...")
            
            # Aplica chunking inteligente
            file_chunks = chunk_text(content, config["chunk_size"], config["overlap"])
            
            # Filtra chunks muito pequenos (menos úteis para busca)
            filtered_chunks = [chunk for chunk in file_chunks if len(chunk.strip()) > 50]
            
            print(f"    📊 {len(content):,} chars → {len(file_chunks)} chunks → {len(filtered_chunks)} úteis")
            
            start_char = 0
            for i, chunk in enumerate(filtered_chunks):
                # Limpa e normaliza o chunk
                clean_chunk = chunk.strip()
                if clean_chunk:
                    chunks.append(clean_chunk)
                    end_char = start_char + len(chunk)
                    metadatas.append(Metadata(
                        source=filepath,
                        chunk_id=i,
                        start_char=start_char,
                        end_char=end_char
                    ))
                    start_char = end_char - config["overlap"]
        
        if not chunks:
            print(f"{Fore.RED}❌ Nenhum chunk válido foi gerado!")
            return
        
        print(f"{Fore.GREEN}✅ Criados {len(chunks)} chunks úteis")
        print(f"  📏 Tamanho médio: {sum(len(c) for c in chunks) // len(chunks)} caracteres")
        print(f"  📊 Distribuição de tamanhos:")
        
        # Mostra distribuição de tamanhos para análise
        sizes = [len(c) for c in chunks]
        sizes.sort()
        print(f"    Mínimo: {min(sizes)} chars")
        print(f"    Mediana: {sizes[len(sizes)//2]} chars")  
        print(f"    Máximo: {max(sizes)} chars")
        
        # Criar embeddings
        print(f"\n{Fore.BLUE}🧠 Carregando modelo de embeddings...")
        print(f"  📦 Modelo: {config['embedding_model']}")
        model = SentenceTransformer(config["embedding_model"])
        
        print(f"{Fore.BLUE}🔄 Gerando embeddings...")
        embeddings = []
        batch_size = 32
        
        for i in tqdm(range(0, len(chunks), batch_size), desc="Processando chunks"):
            batch = chunks[i:i+batch_size]
            batch_embeddings = model.encode(batch, show_progress_bar=False)
            embeddings.extend(batch_embeddings)
        
        embeddings_array = np.array(embeddings).astype('float32')
        print(f"{Fore.GREEN}✅ Embeddings criados: {embeddings_array.shape}")
        
        # Criar índice FAISS
        print(f"\n{Fore.BLUE}🔍 Construindo índice FAISS...")
        dimension = embeddings_array.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine similarity)
        
        # Normalizar embeddings para cosine similarity
        faiss.normalize_L2(embeddings_array)
        index.add(embeddings_array)
        
        print(f"{Fore.GREEN}✅ Índice construído com {index.ntotal} vetores")
        
        # Criar diretórios de saída
        os.makedirs(os.path.dirname(config["index_path"]), exist_ok=True)
        
        # Salvar índice
        print(f"\n{Fore.BLUE}💾 Salvando arquivos...")
        faiss.write_index(index, config["index_path"])
        print(f"✅ Índice salvo em: {config['index_path']}")
        
        # Salvar metadados
        with open(config["meta_path"], "w", encoding="utf-8") as f:
            for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
                data = {
                    "chunk_id": i,
                    "text": chunk,
                    "source": meta.source,
                    "start_char": meta.start_char,
                    "end_char": meta.end_char
                }
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
        print(f"✅ Metadados salvos em: {config['meta_path']}")
        
        # Salvar configurações
        settings = {
            "embedding_model": config["embedding_model"],
            "chunk_size": config["chunk_size"],
            "overlap": config["overlap"],
            "dimension": dimension,
            "total_chunks": len(chunks),
            "total_documents": len(documents),
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(config["settings_path"], "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print(f"✅ Configurações salvas em: {config['settings_path']}")
        
        print(f"\n{Fore.GREEN}🎉 BASE DE CONHECIMENTO CRIADA COM SUCESSO!")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.CYAN}📊 Estatísticas:")
        print(f"  📄 Documentos processados: {len(documents)}")
        print(f"  📝 Chunks criados: {len(chunks)}")
        print(f"  🧠 Dimensão dos embeddings: {dimension}")
        print(f"  💾 Tamanho do índice: {index.ntotal} vetores")
        print(f"\n{Fore.YELLOW}💡 Agora você pode usar a opção 2 para conversar com o chatbot!")
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro durante a construção da base:")
        print(f"{Fore.RED}   {str(e)}")
        print(f"\n{Fore.YELLOW}💡 Tente novamente ou consulte a ajuda (opção 5)")
    
    wait_for_enter()

# ================================
# Chat Interativo
# ================================

def load_meta(meta_path: str) -> list[dict[str, Any]]:
    """Carrega metadados do arquivo JSONL"""
    items = []
    with open(meta_path, "r", encoding="utf-8") as f:
        for line in f:
            items.append(json.loads(line))
    return items

def search_index(query: str, index_path: str, meta_path: str, top_k: int = 3) -> list[Retrieved]:
    """Busca no índice FAISS"""
    config = DEFAULT_CONFIG
    
    # Carregar índice e metadados
    index = faiss.read_index(index_path)
    meta = load_meta(meta_path)
    
    # Criar embedding da query
    model = SentenceTransformer(config["embedding_model"])
    query_embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    
    # Buscar
    scores, indices = index.search(query_embedding, top_k)
    indices = indices[0]
    scores = scores[0]
    
    # Montar resultados
    results: list[Retrieved] = []
    for i, score in zip(indices, scores):
        if i == -1:
            continue
        rec = meta[i]
        metadata = Metadata(
            source=rec["source"],
            chunk_id=rec["chunk_id"],
            start_char=rec["start_char"],
            end_char=rec["end_char"]
        )
        results.append(Retrieved(text=rec["text"], meta=metadata, score=float(score)))
    
    return results

def generate_answer(contexts: list[Retrieved], question: str) -> str:
    """Gera resposta usando RAG + FLAN-T5 híbrido"""
    config = DEFAULT_CONFIG
    
    # Verificar qualidade dos contextos recuperados
    if not contexts:
        print(f"{Fore.YELLOW}🔍 Nenhum contexto encontrado no RAG, usando FLAN-T5...")
        return flan_fallback.generate_fallback_response(question)
    
    # Calcular score médio para decidir usar RAG ou FLAN-T5
    avg_score = sum(ctx.score for ctx in contexts) / len(contexts)
    min_score = min(ctx.score for ctx in contexts)
    
    # Limiar para decidir entre RAG e FLAN-T5
    RAG_THRESHOLD = 0.4
    MIN_SCORE_THRESHOLD = 0.3
    
    if avg_score < RAG_THRESHOLD or min_score < MIN_SCORE_THRESHOLD:
        print(f"{Fore.YELLOW}🤔 Contexto RAG com baixa relevância (score: {avg_score:.2f}), usando FLAN-T5...")
        return flan_fallback.generate_fallback_response(question)
    
    # Usar RAG com contexto de alta qualidade
    print(f"{Fore.GREEN}✅ Usando RAG com contexto relevante (score: {avg_score:.2f})")
    
    # Montar prompt para RAG
    context_text = "\n\n".join([
        f"[DOCUMENTO {i+1} - Relevância: {ctx.score:.2f}]\n{ctx.text}" 
        for i, ctx in enumerate(contexts)
    ])
    
    prompt = f"""Você é um assistente especializado da ICTA Technology. Responda APENAS com base no contexto fornecido abaixo.

IMPORTANTE: 
- Use SOMENTE as informações do contexto
- Se a resposta não estiver clara no contexto, diga que precisa de mais informações
- Seja específico e direto
- Mantenha o foco em BI, automação, IA e integrações

CONTEXTO DA ICTA:
{context_text}

PERGUNTA DO CLIENTE: {question}

RESPOSTA BASEADA NO CONTEXTO:"""
    
    # Carregar modelo se necessário
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(config["generation_model"])
        model = AutoModelForSeq2SeqLM.from_pretrained(config["generation_model"]).to(device)
        
        # Gerar resposta
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=10000).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=config["max_tokens"],
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Limpar resposta
        response = response.replace(prompt, "").strip()
        
        # Adicionar indicador de que foi resposta do RAG
        response += f"\n\n📊 *Resposta baseada na base de conhecimento da ICTA (relevância: {avg_score:.1%})*"
        
        return response
        
    except Exception as e:
        print(f"{Fore.RED}❌ Erro no RAG, usando FLAN-T5 como backup: {e}")
        return flan_fallback.generate_fallback_response(question)

def hybrid_rag_query(query: str, top_k: int = 8) -> tuple[str, str]:
    """Consulta híbrida que combina RAG e FLAN-T5"""
    
    # 1. Tentar buscar no RAG primeiro
    try:
        search_results = search_index(query, "./index/faiss.index", "./index/meta.jsonl", top_k=top_k)
        
        if search_results:
            # Analisar qualidade dos resultados
            scores = [result.score for result in search_results]
            avg_score = sum(scores) / len(scores)
            
            print(f"{Fore.CYAN}🔍 RAG encontrou {len(search_results)} resultados (score médio: {avg_score:.2f})")
            
            # Gerar resposta (decide internamente entre RAG e FLAN-T5)
            answer = generate_answer(search_results, query)
            
            if avg_score >= 0.4:
                return answer, "rag"
            else:
                return answer, "flan_t5_low_rag"
        else:
            print(f"{Fore.YELLOW}🤔 RAG não encontrou resultados, usando FLAN-T5...")
            answer = flan_fallback.generate_fallback_response(query)
            return answer, "flan_t5_no_rag"
            
    except Exception as e:
        print(f"{Fore.RED}❌ Erro no RAG: {e}")
        print(f"{Fore.YELLOW}🔄 Usando FLAN-T5 como fallback...")
        answer = flan_fallback.generate_fallback_response(query)
        return answer, "flan_t5_error"

def print_colored(text: str, color: str = "white"):
    """Imprime texto com cor específica"""
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "blue": Fore.BLUE,
        "yellow": Fore.YELLOW,
        "cyan": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "gray": Fore.LIGHTBLACK_EX
    }
    print(f"{colors.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}")

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def classify_query_intent(question: str) -> dict:
    """Classifica a intenção da pergunta usando palavras-chave simples"""
    try:
        question_lower = question.lower()
        
        # Classificação baseada em palavras-chave
        if any(word in question_lower for word in ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'hello', 'hey']):
            return {"intent": "saudacao", "topic": "saudação", "confidence": "high"}
        
        elif any(word in question_lower for word in ['tchau', 'até logo', 'bye', 'adeus', 'obrigado', 'valeu']):
            return {"intent": "despedida", "topic": "despedida", "confidence": "high"}
        
        elif any(word in question_lower for word in ['totvs', 'integração', 'integrar', 'conectar', 'sistema', 'erp']):
            return {"intent": "integracao", "topic": "integrações com TOTVS", "confidence": "high"}
        
        elif any(word in question_lower for word in ['bi', 'business intelligence', 'relatório', 'dashboard', 'kpi']):
            return {"intent": "bi", "topic": "Business Intelligence", "confidence": "high"}
        
        elif any(word in question_lower for word in ['automação', 'automatizar', 'processo', 'workflow']):
            return {"intent": "automacao", "topic": "automação de processos", "confidence": "high"}
        
        elif any(word in question_lower for word in ['ia', 'inteligência artificial', 'machine learning', 'ai']):
            return {"intent": "ia", "topic": "inteligência artificial", "confidence": "high"}
        
        elif any(word in question_lower for word in ['serviço', 'oferecem', 'fazem', 'trabalham', 'consultoria']):
            return {"intent": "servicos", "topic": "serviços da ICTA", "confidence": "high"}
        
        else:
            return {"intent": "geral", "topic": "informações gerais", "confidence": "medium"}
            
    except Exception as e:
        print_colored(f"❌ Erro na classificação: {e}", "red")
        return {"intent": "geral", "topic": "informações gerais", "confidence": "low"}

def generate_guided_response(contexts: list, question: str, intent_info: dict) -> str:
    """Gera resposta guiada com interação usando FLAN-T5"""
    try:
        config = DEFAULT_CONFIG
        model_name = config["generation_model"]
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        
        # Verifica se há contextos relevantes
        if not contexts or all(ctx.score < 0.3 for ctx in contexts):
            # Sem contextos relevantes - resposta conversacional simples
            if intent_info.get('intent') == 'saudacao':
                return "Olá! 👋 Sou o assistente da ICTA Technology. Como posso ajudar você hoje? Posso esclarecer dúvidas sobre nossos serviços de BI, automação e IA!"
            elif intent_info.get('intent') == 'despedida':
                return "Até logo! 👋 Foi um prazer ajudar. Se precisar de mais alguma coisa sobre BI, automação ou IA, estarei aqui!"
            else:
                guidance_prompt = f"""Você é um assistente da ICTA Technology. Responda de forma conversacional e útil.

Pergunta: {question}
Tópico: {intent_info.get('topic', 'geral')}

Responda de forma amigável, faça perguntas se necessário, e sugira como podemos ajudar.

Resposta:"""
        else:
            # Com contextos - resposta com base no conteúdo
            context_text = "\n".join([f"- {ctx.text[:200]}..." for ctx in contexts[:2]])
            
            guidance_prompt = f"""Baseado no contexto, responda a pergunta de forma conversacional e útil.

Contexto: {context_text}
Pergunta: {question}

Resposta conversacional:"""
        
        inputs = tokenizer(guidance_prompt, return_tensors="pt", max_length=10000, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=400,
                temperature=0.5,
                do_sample=True,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        # Limpar a resposta removendo o prompt
        if "Resposta:" in response:
            response = response.split("Resposta:")[-1].strip()
        
        return response if response else "Desculpe, não consegui gerar uma resposta adequada. Pode reformular sua pergunta?"
        
    except Exception as e:
        print_colored(f"❌ Erro na geração de resposta: {e}", "red")
        
        # Fallback simples baseado na intenção
        if intent_info.get('intent') == 'saudacao':
            return "Olá! 👋 Sou o assistente da ICTA Technology. Como posso ajudar?"
        elif intent_info.get('intent') == 'despedida':
            return "Até logo! 👋 Obrigado por usar nossos serviços!"
        else:
            return f"Entendi que você está perguntando sobre {intent_info.get('topic', 'nossos serviços')}. Pode me dar mais detalhes para te ajudar melhor?"

def suggest_related_topics(intent: str) -> list[str]:
    """Sugere tópicos relacionados baseado na intenção"""
    topic_suggestions = {
        "servicos": [
            "Quais são os principais serviços de BI?",
            "Como funciona a automação de processos?",
            "Que tipos de IA vocês implementam?"
        ],
        "integracao": [
            "Quais módulos TOTVS vocês integram?",
            "Como é feita a migração de dados?",
            "Qual o tempo de implementação?"
        ],
        "bi": [
            "Que ferramentas de BI vocês usam?",
            "Como criar dashboards personalizados?",
            "Quais relatórios estão disponíveis?"
        ],
        "automacao": [
            "Que processos podem ser automatizados?",
            "Qual o ROI da automação?",
            "Como funciona a implementação?"
        ],
        "ia": [
            "Que tipos de IA vocês desenvolvem?",
            "Como a IA pode ajudar meu negócio?",
            "Quais são os casos de uso mais comuns?"
        ]
    }
    
    return topic_suggestions.get(intent, [
        "Quais são os principais serviços da ICTA?",
        "Como posso entrar em contato?",
        "Que tipos de projetos vocês fazem?"
    ])

def interactive_chat():
    """Chat interativo simples e limpo"""
    print_colored("\n💬 CHAT ICTA TECHNOLOGY", "cyan")
    print_colored("=" * 50, "cyan")
    
    # Verificar se há base de conhecimento (silenciosamente)
    rag_available = os.path.exists("./index/faiss.index")
    
    if not rag_available:
        print_colored("⚠️ Para melhor experiência, construa a base de conhecimento primeiro (opção 1)", "yellow")
    
    print_colored("\n🤖 Olá! Sou o assistente da ICTA Technology.", "green")
    print_colored("💡 Posso ajudar com dúvidas sobre BI, automação, IA e integrações.", "blue")
    print_colored("\n📝 Digite sua pergunta (ou 'sair' para encerrar):", "white")
    
    conversation_history = []
    
    while True:
        print_colored("\n" + "─" * 50, "gray")
        user_input = input(f"{Fore.YELLOW}👤 Você: {Style.RESET_ALL}").strip()
        
        if user_input.lower() in ['sair', 'exit', 'quit', 'bye']:
            print_colored("\n👋 Obrigado por usar o assistente ICTA! Até logo!", "green")
            break
        
        if not user_input:
            print_colored("❓ Por favor, digite uma pergunta.", "yellow")
            continue
        
        # Salvar pergunta do usuário
        conversation_history.append({"role": "user", "content": user_input, "timestamp": datetime.now().isoformat()})
        
        # Processar pergunta silenciosamente (sem mostrar detalhes técnicos)
        try:
            if rag_available:
                # Tentar RAG primeiro
                search_results = search_index(user_input, "./index/faiss.index", "./index/meta.jsonl", top_k=8)
                
                if search_results:
                    # Avaliar qualidade silenciosamente
                    scores = [result.score for result in search_results]
                    avg_score = sum(scores) / len(scores)
                    
                    # Usar RAG + FLAN-T5 se qualidade é boa
                    if avg_score >= 0.4:
                        # RAG context + FLAN-T5 processing
                        answer = generate_enhanced_answer_with_context(search_results, user_input)
                    else:
                        # Apenas FLAN-T5 sem contexto RAG
                        answer = generate_enhanced_answer_without_context(user_input)
                else:
                    # Sem resultados RAG, usar apenas FLAN-T5
                    answer = generate_enhanced_answer_without_context(user_input)
            else:
                # Apenas FLAN-T5 sem RAG
                answer = generate_enhanced_answer_without_context(user_input)
                
        except Exception:
            # Em caso de erro, usar resposta padrão
            answer = "Para informações específicas sobre nossos serviços, entre em contato com nossa equipe da ICTA Technology."
        
        # Exibir apenas a resposta, sem informações técnicas
        print_colored(f"\n🤖 ICTA Assistant:", "cyan")
        print_colored(answer, "white")
        
        # Salvar resposta
        conversation_history.append({
            "role": "assistant", 
            "content": answer,
            "timestamp": datetime.now().isoformat()
        })
    
    # Salvar histórico silenciosamente
    save_conversation_history(conversation_history)
    wait_for_enter()

def generate_enhanced_answer_with_context(contexts: list[Retrieved], question: str) -> str:
    """Usa modelo português para processar RAG + pergunta"""
    try:
        if not contexts:
            return generate_enhanced_answer_without_context(question)
        
        # Extrair contexto dos melhores resultados
        context_parts = []
        for ctx in contexts[:5]:  # Usar os 5 melhores
            context_parts.append(ctx.text.strip())
        
        rag_context = "\n\n".join(context_parts)
        
        # Usar modelo português para resposta melhor
        response = portuguese_llm.generate_enhanced_response(question, rag_context)
        
        return response
        
    except Exception:
        # Fallback para RAG direto se houver erro
        return contexts[0].text if contexts else "Entre em contato para mais informações sobre os serviços da ICTA Technology."

def generate_enhanced_answer_without_context(question: str) -> str:
    """Usa modelo português para perguntas gerais"""
    try:
        # Usar modelo português diretamente
        response = portuguese_llm.generate_enhanced_response(question)
        
        # Se a resposta for muito genérica, usar FLAN-T5 como fallback
        if len(response) < 20 or "Entre em contato" in response:
            # Criar respostas personalizadas para cumprimentos
            if any(word in question.lower() for word in ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite']):
                return "Olá! Sou o assistente da ICTA Technology. Posso ajudar com informações sobre Business Intelligence, automação de processos e inteligência artificial. Como posso ajudá-lo?"
            
            if 'icta' in question.lower():
                return "A ICTA Technology é uma consultoria especializada em Business Intelligence, automação de processos, inteligência artificial e integrações com sistemas ERP. Oferecemos soluções personalizadas para empresas."
        
        return response
        
    except Exception:
        return "Posso ajudar com informações sobre os serviços da ICTA Technology. O que gostaria de saber?"
    
    conversation_history = []
    response_stats = {"rag": 0, "flan_t5_low_rag": 0, "flan_t5_no_rag": 0, "flan_t5_error": 0}
    
    while True:
        print_colored("\n" + "─" * 50, "gray")
        user_input = input(f"{Fore.YELLOW}👤 Você: {Style.RESET_ALL}").strip()
        
        if user_input.lower() in ['sair', 'exit', 'quit', 'bye']:
            print_colored("\n� ESTATÍSTICAS DA CONVERSA:", "cyan")
            print_colored(f"   🎯 Respostas RAG: {response_stats['rag']}", "green")
            print_colored(f"   🤖 Respostas FLAN-T5 (baixa relevância): {response_stats['flan_t5_low_rag']}", "yellow")
            print_colored(f"   🧠 Respostas FLAN-T5 (sem contexto): {response_stats['flan_t5_no_rag']}", "blue")
            print_colored(f"   🔧 Fallback por erro: {response_stats['flan_t5_error']}", "red")
            print_colored("\n�👋 Obrigado por usar o assistente híbrido ICTA! Até logo!", "green")
            break
        
        if not user_input:
            print_colored("❓ Por favor, digite uma pergunta.", "yellow")
            continue
        
        # Salvar pergunta do usuário
        conversation_history.append({"role": "user", "content": user_input, "timestamp": datetime.now().isoformat()})
        
        print_colored(f"{Fore.CYAN}🔍 Processando pergunta...", "cyan")
        
        # Usar sistema híbrido
        if rag_available:
            try:
                answer, source_type = hybrid_rag_query(user_input, top_k=8)
                response_stats[source_type] += 1
                
                # Indicador visual do tipo de resposta
                if source_type == "rag":
                    indicator = "🎯 RAG"
                elif source_type == "flan_t5_low_rag":
                    indicator = "🤖 FLAN-T5 (baixa relevância RAG)"
                elif source_type == "flan_t5_no_rag":
                    indicator = "🧠 FLAN-T5 (sem contexto RAG)"
                else:
                    indicator = "🔧 FLAN-T5 (fallback)"
                
                print_colored(f"   Fonte: {indicator}", "gray")
                
            except Exception as e:
                print_colored(f"❌ Erro no sistema híbrido: {e}", "red")
                answer = flan_fallback.generate_fallback_response(user_input)
                response_stats["flan_t5_error"] += 1
        else:
            # Apenas FLAN-T5 se não há RAG
            print_colored("   🧠 Usando apenas FLAN-T5 (sem RAG)", "yellow")
            answer = flan_fallback.generate_fallback_response(user_input)
            response_stats["flan_t5_no_rag"] += 1
        
        # Exibir resposta
        print_colored(f"\n🤖 ICTA Assistant:", "cyan")
        print_colored(answer, "white")
        
        # Perguntar feedback para melhoria contínua
        print_colored(f"\n💭 Esta resposta foi útil? (s/n/parcial): ", "gray", end="")
        try:
            feedback = input().strip().lower()
            if feedback in ['n', 'não', 'nao']:
                print_colored("� Vou tentar uma abordagem diferente na próxima!", "blue")
            elif feedback in ['parcial', 'mais ou menos']:
                print_colored("📝 Entendi, vou me esforçar para ser mais preciso!", "yellow")
            elif feedback in ['s', 'sim', 'yes']:
                print_colored("😊 Fico feliz em ajudar!", "green")
        except KeyboardInterrupt:
            break
        
        # Salvar resposta com metadados
        conversation_history.append({
            "role": "assistant", 
            "content": answer,
            "source_type": source_type if rag_available else "flan_t5_only",
            "feedback": feedback if 'feedback' in locals() else None,
            "timestamp": datetime.now().isoformat()
        })
    
    # Salvar histórico
    save_conversation_history(conversation_history)
    wait_for_enter()

def save_conversation_history(history: list):
    """Salva o histórico da conversa"""
    try:
        os.makedirs("./history", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = f"./history/chat_{timestamp}.json"
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        print_colored(f"💾 Conversa salva em: {history_file}", "green")
    except Exception as e:
        print_colored(f"❌ Erro ao salvar histórico: {e}", "red")

def start_chat():
    """Inicia o chat interativo inteligente"""
    interactive_chat()

# ================================
# Configurações
# ================================

def show_settings():
    """Mostra e permite alterar configurações básicas"""
    print(f"\n{Fore.GREEN}⚙️ CONFIGURAÇÕES DO SISTEMA")
    print(f"{Fore.GREEN}{'='*40}")
    
    config = DEFAULT_CONFIG
    
    print(f"\n{Fore.CYAN}📋 Configurações atuais:")
    print(f"  1. Modelo de embeddings: {config['embedding_model']}")
    print(f"  2. Modelo de geração: {config['generation_model']}")
    print(f"  3. Tamanho do chunk: {config['chunk_size']} caracteres")
    print(f"  4. Sobreposição: {config['overlap']} caracteres")
    print(f"  5. Documentos por busca: {config['top_k']}")
    print(f"  6. Tokens máximos na resposta: {config['max_tokens']}")
    
    print(f"\n{Fore.YELLOW}💡 Dicas:")
    print(f"• Chunks menores = busca mais precisa, mas pode perder contexto")
    print(f"• Mais documentos por busca = respostas mais completas")
    print(f"• Mais tokens = respostas mais longas")
    
    print(f"\n{Fore.LIGHTBLACK_EX}ℹ️ Para alterar configurações, edite o arquivo de código")
    print(f"ℹ️ Após alterações, reconstrua a base de conhecimento")
    
    wait_for_enter()

# ================================
# Sistema de Ajuda
# ================================

def show_help():
    """Sistema de ajuda interativo"""
    while True:
        print(f"\n{Fore.CYAN}📚 CENTRAL DE AJUDA")
        print(f"{Fore.CYAN}{'='*40}")
        
        print_menu_option(1, "❓ Como começar", 
                         "Primeiros passos para usar o sistema")
        
        print_menu_option(2, "📁 Preparar documentos", 
                         "Como organizar seus arquivos .jsonl")
        
        print_menu_option(3, "🔧 Solução de problemas", 
                         "Erros comuns e soluções")
        
        print_menu_option(4, "💡 Dicas de uso", 
                         "Como obter melhores resultados")
        
        print_menu_option(5, "📖 Sobre o projeto", 
                         "Informações técnicas")
        
        print_menu_option(6, "🔙 Voltar", 
                         "Retorna ao menu principal")
        
        choice = get_user_choice(6)
        
        if choice == 1:
            show_getting_started()
        elif choice == 2:
            show_document_guide()
        elif choice == 3:
            show_troubleshooting()
        elif choice == 4:
            show_usage_tips()
        elif choice == 5:
            show_about()
        elif choice == 6:
            break

def show_getting_started():
    """Guia de primeiros passos"""
    print(f"\n{Fore.GREEN}🚀 PRIMEIROS PASSOS")
    print(f"{Fore.GREEN}{'='*30}")
    print(f"""
{Fore.CYAN}Passo 1: Preparar documentos{Style.RESET_ALL}
• Crie/verifique a pasta 'data' no diretório do programa
• Adicione arquivos .jsonl com suas FAQs e documentos
• Use formato claro: "P: pergunta R: resposta"

{Fore.CYAN}Passo 2: Construir base de conhecimento{Style.RESET_ALL}
• No menu principal, escolha opção 1
• Aguarde o processamento dos documentos
• Isso criará um índice de busca inteligente

{Fore.CYAN}Passo 3: Conversar com o chatbot{Style.RESET_ALL}
• No menu principal, escolha opção 2
• Digite suas perguntas naturalmente
• O sistema buscará as melhores respostas

{Fore.YELLOW}🎯 Dica: Comece com poucos documentos para testar!{Style.RESET_ALL}
    """)
    wait_for_enter()

def show_document_guide():
    """Guia para preparação de documentos"""
    print(f"\n{Fore.GREEN}📁 GUIA DE DOCUMENTOS")
    print(f"{Fore.GREEN}{'='*30}")
    print(f"""
{Fore.CYAN}Estrutura recomendada:{Style.RESET_ALL}
data/
├── faq_geral.jsonl
├── produtos.jsonl
├── suporte.jsonl
└── politicas.jsonl

{Fore.CYAN}Formato dos arquivos .jsonl:{Style.RESET_ALL}
{"id": "faq-001", "source": "faq_geral", "question": "Como funciona o sistema?", "answer": "Nosso sistema utiliza inteligência artificial..."}
{"id": "faq-002", "source": "faq_geral", "question": "Quais são os preços?", "answer": "Oferecemos planos a partir de R$ 99/mês..."}

{Fore.CYAN}Boas práticas:{Style.RESET_ALL}
• Use linguagem clara e direta
• Inclua palavras-chave importantes
• Evite textos muito longos
• Organize por temas em arquivos separados
• Teste com perguntas reais dos usuários

{Fore.YELLOW}💡 Exemplo de bom formato:{Style.RESET_ALL}
P: Como entrar em contato?
R: Entre em contato pelo WhatsApp (11) 99999-9999 ou 
email contato@ictatechnology.com. Atendemos de segunda 
a sexta das 9h às 18h.
    """)
    wait_for_enter()

def show_troubleshooting():
    """Guia de solução de problemas"""
    print(f"\n{Fore.GREEN}🔧 SOLUÇÃO DE PROBLEMAS")
    print(f"{Fore.GREEN}{'='*35}")
    print(f"""
{Fore.RED}❌ "Nenhum arquivo .jsonl encontrado"{Style.RESET_ALL}
• Verifique se a pasta 'data' existe
• Confirme que há arquivos .jsonl na pasta
• Verifique se os arquivos não estão vazios

{Fore.RED}❌ "Modelo não encontrado"{Style.RESET_ALL}
• Primeira execução precisa de internet
• Aguarde o download dos modelos (pode demorar)
• Verifique sua conexão com a internet

{Fore.RED}❌ "Erro de memória"{Style.RESET_ALL}
• Feche outros programas pesados
• Use um modelo menor (flan-t5-small)
• Reduza o tamanho dos chunks no código

{Fore.RED}❌ "Respostas ruins"{Style.RESET_ALL}
• Melhore a qualidade dos documentos
• Use textos mais específicos
• Adicione mais exemplos similares
• Verifique se as palavras-chave estão corretas

{Fore.YELLOW}🆘 Precisa de mais ajuda?{Style.RESET_ALL}
• GitHub: https://github.com/jesseff20/rag-chatbot
• Issues: reporte problemas no GitHub
• Email: contato@ictatechnology.com
    """)
    wait_for_enter()

def show_usage_tips():
    """Dicas de uso avançado"""
    print(f"\n{Fore.GREEN}💡 DICAS DE USO AVANÇADO")
    print(f"{Fore.GREEN}{'='*35}")
    print(f"""
{Fore.CYAN}📝 Para melhores documentos:{Style.RESET_ALL}
• Use perguntas que seus clientes realmente fazem
• Inclua sinônimos e variações
• Mantenha respostas focadas e diretas
• Atualize regularmente o conteúdo

{Fore.CYAN}🔍 Para melhores buscas:{Style.RESET_ALL}
• Use palavras-chave específicas
• Faça perguntas completas, não apenas palavras
• Seja específico sobre o que quer saber
• Reformule se não conseguir boa resposta

{Fore.CYAN}⚙️ Para melhor performance:{Style.RESET_ALL}
• Organize documentos por tema
• Mantenha arquivos com tamanho moderado
• Remova informações duplicadas
• Teste regularmente a qualidade

{Fore.CYAN}🎯 Para casos específicos:{Style.RESET_ALL}
• FAQ geral: use linguagem informal
• Documentação técnica: seja preciso
• Atendimento: inclua contatos e horários
• Produtos: especificações e preços atuais

{Fore.YELLOW}🔄 Lembre-se: após mudanças nos documentos,{Style.RESET_ALL}
{Fore.YELLOW}reconstrua a base de conhecimento (opção 1)!{Style.RESET_ALL}
    """)
    wait_for_enter()

def show_about():
    """Informações sobre o projeto"""
    print(f"\n{Fore.GREEN}📖 SOBRE O PROJETO")
    print(f"{Fore.GREEN}{'='*30}")
    print(f"""
{Fore.CYAN}RAG Chatbot ICTA Technology{Style.RESET_ALL}
Versão: 2.0 - Interface Simplificada
Data: Agosto 2025

{Fore.CYAN}👨‍💻 Desenvolvido por:{Style.RESET_ALL}
Jesse Fernandes
ICTA Technology
Email: jesse.fernandes@ictatechnology.com

{Fore.CYAN}🔧 Tecnologias utilizadas:{Style.RESET_ALL}
• FAISS - Busca vetorial Facebook AI
• Sentence Transformers - Embeddings de texto
• FLAN-T5 - Modelo de linguagem Google
• Python 3.8+ - Linguagem de programação

{Fore.CYAN}✨ Características:{Style.RESET_ALL}
• 100% local (sem APIs pagas)
• Interface amigável e interativa
• Configuração automática
• Suporte a múltiplos documentos
• Histórico de conversas

{Fore.CYAN}📄 Licença:{Style.RESET_ALL}
MIT License - Uso livre e modificação permitida

{Fore.CYAN}🌐 Links importantes:{Style.RESET_ALL}
• GitHub: https://github.com/jesseff20/rag-chatbot
• Issues: https://github.com/jesseff20/rag-chatbot/issues
• Documentação: Arquivo README.md

{Fore.YELLOW}💝 Desenvolvido com ❤️ para a comunidade!{Style.RESET_ALL}
{Fore.YELLOW}Contribuições e sugestões são bem-vindas.{Style.RESET_ALL}
    """)
    wait_for_enter()

# ================================
# Função Principal
# ================================

def main():
    """Função principal com menu interativo"""
    # Configuração inicial
    print_header()
    
    # Loop principal
    while True:
        show_main_menu()
        choice = get_user_choice(6)
        
        if choice == 1:
            build_knowledge_base()
        elif choice == 2:
            start_chat()
        elif choice == 3:
            check_system_status()
        elif choice == 4:
            show_settings()
        elif choice == 5:
            show_help()
        elif choice == 6:
            print(f"\n{Fore.GREEN}👋 Obrigado por usar o RAG Chatbot ICTA!")
            print(f"{Fore.GREEN}Até logo!")
            break

if __name__ == "__main__":
    main()
