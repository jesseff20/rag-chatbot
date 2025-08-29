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
    "chunk_size": 800,
    "overlap": 120,
    "top_k": 3,
    "max_tokens": 150,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "generation_model": "google/flan-t5-base"
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

def read_text_files(folder: str) -> dict[str, str]:
    """Lê todos os .txt do diretório"""
    print(f"{Fore.BLUE}📂 Lendo arquivos .txt de: {folder}")
    
    if not os.path.exists(folder):
        print(f"{Fore.RED}❌ Diretório não encontrado: {folder}")
        return {}
    
    data: dict[str, str] = {}
    txt_files = []
    
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".txt"):
                txt_files.append(os.path.join(root, f))
    
    if not txt_files:
        print(f"{Fore.YELLOW}⚠️ Nenhum arquivo .txt encontrado em {folder}")
        return {}
    
    print(f"{Fore.GREEN}📄 Encontrados {len(txt_files)} arquivos .txt")
    
    for fp in tqdm(txt_files, desc="Lendo arquivos"):
        try:
            with open(fp, "r", encoding="utf-8") as fh:
                content = fh.read().strip()
            if content:
                data[fp] = content
                print(f"{Fore.GREEN}  ✅ {os.path.basename(fp)} ({len(content)} caracteres)")
            else:
                print(f"{Fore.YELLOW}  ⚠️ {os.path.basename(fp)} está vazio")
        except Exception as e:
            print(f"{Fore.RED}  ❌ Erro ao ler {os.path.basename(fp)}: {e}")
    
    return data

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    """Quebra texto em chunks com sobreposição"""
    chunks = []
    start = 0
    n = len(text)
    
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        if end == n:
            break
        start = end - overlap
        if start < 0:
            start = 0
    
    return chunks

# ================================
# Menu Principal
# ================================

def show_main_menu():
    """Exibe o menu principal"""
    print(f"\n{Fore.CYAN}📋 MENU PRINCIPAL")
    print(f"{Fore.CYAN}{'='*50}")
    
    print_menu_option(1, "🏗️ Construir Base de Conhecimento", 
                     "Processa seus arquivos .txt e cria o índice de busca")
    
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
        txt_files = [f for f in os.listdir(config["docs_path"]) if f.endswith('.txt')]
        if txt_files:
            print(f"  ✅ {len(txt_files)} arquivos .txt encontrados:")
            for f in txt_files[:5]:  # Mostrar apenas os primeiros 5
                print(f"    📝 {f}")
            if len(txt_files) > 5:
                print(f"    ... e mais {len(txt_files) - 5} arquivos")
        else:
            print(f"  ⚠️ Nenhum arquivo .txt encontrado em {config['docs_path']}")
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
        print("  • Crie o diretório 'data' e adicione arquivos .txt")
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
            print(f"{Fore.YELLOW}💡 Adicione seus arquivos .txt em '{config['docs_path']}' e tente novamente")
            wait_for_enter()
            return
        else:
            return
    
    # Ler arquivos
    documents = read_text_files(config["docs_path"])
    if not documents:
        print(f"{Fore.RED}❌ Nenhum arquivo .txt encontrado ou todos estão vazios!")
        print(f"{Fore.YELLOW}💡 Adicione arquivos .txt em '{config['docs_path']}' e tente novamente")
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
        # Criar chunks
        print(f"\n{Fore.BLUE}📝 Dividindo textos em chunks...")
        chunks: list[str] = []
        metadatas: list[Metadata] = []
        
        for filepath, content in documents.items():
            print(f"  📝 Processando {os.path.basename(filepath)}...")
            file_chunks = chunk_text(content, config["chunk_size"], config["overlap"])
            print(f"    📊 {len(content)} chars → {len(file_chunks)} chunks")
            
            start_char = 0
            for i, chunk in enumerate(file_chunks):
                chunks.append(chunk)
                end_char = start_char + len(chunk)
                metadatas.append(Metadata(
                    source=filepath,
                    chunk_id=i,
                    start_char=start_char,
                    end_char=end_char
                ))
                start_char = end_char - config["overlap"]
        
        print(f"{Fore.GREEN}✅ Criados {len(chunks)} chunks")
        
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
    """Gera resposta usando FLAN-T5"""
    config = DEFAULT_CONFIG
    
    # Montar prompt
    context_text = "\n\n".join([
        f"[DOCUMENTO {i+1}]\n{ctx.text}" 
        for i, ctx in enumerate(contexts)
    ])
    
    prompt = f"""Você é um assistente da ICTA Technology. Responda APENAS com base no contexto fornecido. Se a resposta não estiver no contexto, diga que não sabe e sugira contato com um humano.

CONTEXTO:
{context_text}

PERGUNTA: {question}

RESPOSTA:"""
    
    # Carregar modelo
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(config["generation_model"])
        model = AutoModelForSeq2SeqLM.from_pretrained(config["generation_model"]).to(device)
        
        # Gerar resposta
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=config["max_tokens"],
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.strip()
        
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

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
    """Classifica a intenção da pergunta usando FLAN-T5"""
    try:
        config = DEFAULT_CONFIG
        model_name = config["generation_model"]
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        
        # Prompt para classificação de intenção
        classification_prompt = f"""Analise esta pergunta e classifique em uma das categorias:
CATEGORIAS: servicos, integracao, bi, automacao, ia, geral, saudacao, despedida, unclear

Pergunta: "{question}"

Categoria:"""
        
        inputs = tokenizer(classification_prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=50,
                temperature=0.3,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        intent = tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower()
        
        # Mapear intenções para tópicos
        intent_mapping = {
            "servicos": "serviços oferecidos pela ICTA",
            "integracao": "integrações com TOTVS",
            "bi": "Business Intelligence e relatórios",
            "automacao": "automação de processos",
            "ia": "inteligência artificial",
            "geral": "informações gerais da empresa",
            "saudacao": "saudação",
            "despedida": "despedida",
            "unclear": "não está claro"
        }
        
        return {
            "intent": intent,
            "topic": intent_mapping.get(intent, "informações gerais"),
            "confidence": "high" if intent in intent_mapping else "low"
        }
        
    except Exception as e:
        print_colored(f"❌ Erro na classificação: {e}", "red")
        return {"intent": "unclear", "topic": "informações gerais", "confidence": "low"}

def generate_clarification_questions(intent_info: dict, original_question: str) -> str:
    """Gera perguntas de esclarecimento usando FLAN-T5"""
    try:
        config = DEFAULT_CONFIG
        model_name = config["generation_model"]
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        
        # Prompt para gerar perguntas de esclarecimento
        clarification_prompt = f"""Você é um assistente da ICTA Technology, empresa de consultoria em BI, automação e IA.

A pergunta do usuário "{original_question}" não está clara sobre o tópico "{intent_info['topic']}".

Faça 2-3 perguntas específicas para ajudar a entender melhor o que o usuário precisa sobre este tópico.

Perguntas de esclarecimento:"""
        
        inputs = tokenizer(clarification_prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=200,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        questions = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return questions
        
    except Exception as e:
        print_colored(f"❌ Erro na geração de perguntas: {e}", "red")
        return "Pode me dar mais detalhes sobre o que você precisa?"

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
            # Sem contextos relevantes - guiar o usuário
            guidance_prompt = f"""Você é um assistente da ICTA Technology.

O usuário perguntou: "{question}"
Tópico identificado: {intent_info['topic']}

Não encontrei informações específicas sobre isso. 

Como assistente especializado em BI, automação e IA, ofereça ajuda alternativa:
1. Sugira tópicos relacionados que podem interessar
2. Faça perguntas para entender melhor a necessidade
3. Ofereça opções de contato se necessário

Resposta útil:"""
        else:
            # Com contextos - resposta normal melhorada
            context_text = "\n".join([f"- {ctx.text[:200]}..." for ctx in contexts[:3]])
            
            guidance_prompt = f"""Você é um assistente especializado da ICTA Technology.

Pergunta: {question}
Contexto encontrado:
{context_text}

Com base no contexto, forneça uma resposta completa e útil. Se a informação não for suficiente, faça perguntas para ajudar melhor o usuário.

Resposta:"""
        
        inputs = tokenizer(guidance_prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=300,
                temperature=0.6,
                do_sample=True,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return response
        
    except Exception as e:
        print_colored(f"❌ Erro na geração de resposta: {e}", "red")
        return "Desculpe, houve um erro. Pode reformular sua pergunta?"

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
    """Chat interativo melhorado com guias inteligentes"""
    print_colored("\n💬 CHAT INTERATIVO ICTA", "cyan")
    print_colored("=" * 50, "cyan")
    
    # Verificar se há base de conhecimento
    if not os.path.exists("./index/faiss.index"):
        print_colored("❌ Base de conhecimento não encontrada!", "red")
        print_colored("   Execute a opção 1 primeiro para construir a base.", "yellow")
        wait_for_enter()
        return
    
    print_colored("🤖 Olá! Sou o assistente da ICTA Technology.", "green")
    print_colored("💡 Posso ajudar com dúvidas sobre BI, automação e IA.", "blue")
    print_colored("🔍 Se não souber responder, vou te guiar para encontrar o que precisa!", "blue")
    print_colored("\n📝 Digite sua pergunta (ou 'sair' para encerrar):", "white")
    
    conversation_history = []
    
    while True:
        print_colored("\n" + "─" * 50, "gray")
        user_input = input(f"{Fore.YELLOW}👤 Você: {Style.RESET_ALL}").strip()
        
        if user_input.lower() in ['sair', 'exit', 'quit', 'bye']:
            print_colored("👋 Obrigado por usar o assistente ICTA! Até logo!", "green")
            break
        
        if not user_input:
            print_colored("❓ Por favor, digite uma pergunta.", "yellow")
            continue
        
        # Salvar pergunta do usuário
        conversation_history.append({"role": "user", "content": user_input})
        
        print_colored(f"\n🔍 Analisando sua pergunta...", "blue")
        
        # 1. Classificar intenção da pergunta
        intent_info = classify_query_intent(user_input)
        
        # 2. Buscar no índice
        try:
            search_results = search_index(user_input, "./index/faiss.index", "./index/meta.jsonl", top_k=3)
        except Exception as e:
            print_colored(f"❌ Erro na busca: {e}", "red")
            search_results = []
        
        # 3. Verificar qualidade dos resultados
        has_good_results = search_results and any(result.score > 0.4 for result in search_results)
        
        if has_good_results:
            # Resposta normal com contexto
            print_colored(f"💡 Encontrei informações relevantes!", "green")
            answer = generate_guided_response(search_results, user_input, intent_info)
        else:
            # Sem resultados bons - modo interativo
            print_colored(f"🤔 Hmm, não encontrei uma resposta específica...", "yellow")
            print_colored(f"📋 Identifiquei que você está perguntando sobre: {intent_info['topic']}", "blue")
            
            # Gerar resposta guiada
            answer = generate_guided_response([], user_input, intent_info)
            
            # Adicionar sugestões de tópicos
            suggestions = suggest_related_topics(intent_info['intent'])
            if suggestions:
                answer += f"\n\n💡 Você pode me perguntar sobre:\n"
                for i, suggestion in enumerate(suggestions, 1):
                    answer += f"   {i}. {suggestion}\n"
        
        # Exibir resposta
        print_colored(f"\n🤖 ICTA Assistant:", "cyan")
        print_colored(answer, "white")
        
        # Salvar resposta
        conversation_history.append({"role": "assistant", "content": answer})
        
        # Perguntar se ajudou
        print_colored(f"\n❓ Esta resposta foi útil? (s/n/mais)", "blue")
        feedback = input(f"{Fore.YELLOW}📝 Feedback: {Style.RESET_ALL}").strip().lower()
        
        if feedback == 'n' or feedback == 'nao':
            print_colored("🔄 Vou tentar ajudar de outra forma!", "blue")
            clarification = generate_clarification_questions(intent_info, user_input)
            print_colored(f"\n🎯 Para te ajudar melhor:", "cyan")
            print_colored(clarification, "white")
        elif feedback == 'mais':
            print_colored("🔍 Pode fazer uma pergunta mais específica sobre o mesmo tópico!", "blue")
    
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
                         "Como organizar seus arquivos .txt")
        
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
• Adicione arquivos .txt com suas FAQs e documentos
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
├── faq_geral.txt
├── produtos.txt
├── suporte.txt
└── politicas.txt

{Fore.CYAN}Formato dos arquivos .txt:{Style.RESET_ALL}
P: Como funciona o sistema?
R: Nosso sistema utiliza inteligência artificial...

P: Quais são os preços?
R: Oferecemos planos a partir de R$ 99/mês...

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
{Fore.RED}❌ "Nenhum arquivo .txt encontrado"{Style.RESET_ALL}
• Verifique se a pasta 'data' existe
• Confirme que há arquivos .txt na pasta
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
