
from __future__ import annotations
import os
import json
import argparse
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

import faiss  # type: ignore
import numpy as np
from tqdm import tqdm
from colorama import Fore, Style

# Embeddings
from sentence_transformers import SentenceTransformer

# Geração local (FLAN-T5)
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# (Opcional) Cliente simples para TGI (Text Generation Inference)
import requests


# ================================
# Utilitários
# ================================

def read_text_files(folder: str) -> Dict[str, str]:
    """Lê todos os .txt do diretório e devolve {filepath: content}.
    Ignora arquivos vazios.
    """
    data: Dict[str, str] = {}
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".txt"):
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8") as fh:
                        content = fh.read().strip()
                    if content:
                        data[fp] = content
                except Exception as e:
                    print(f"[WARN] Falha ao ler {fp}: {e}")
    return data


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    """Quebra texto em janelas de caracteres com sobreposição simples.
    Simples e suficiente para FAQs curtas.
    """
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
# Indexação (FAISS + SentenceTransformer)
# ================================

def build_faiss_index(docs_folder: str, index_path: str, meta_path: str,
                      embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                      chunk_size: int = 800, overlap: int = 120) -> None:
    print(Fore.CYAN + "[1/3] Lendo .txt do corpus..." + Style.RESET_ALL)
    raw_docs = read_text_files(docs_folder)
    if not raw_docs:
        raise SystemExit("Nenhum .txt encontrado em " + docs_folder)

    print(Fore.CYAN + "[2/3] Quebrando em chunks..." + Style.RESET_ALL)
    chunks: List[str] = []
    metadatas: List[Metadata] = []
    for path, content in raw_docs.items():
        offs = 0
        local_chunks = chunk_text(content, chunk_size=chunk_size, overlap=overlap)
        for i, ch in enumerate(local_chunks):
            start_char = offs
            end_char = offs + len(ch)
            chunks.append(ch)
            metadatas.append(Metadata(source=path, chunk_id=i, start_char=start_char, end_char=end_char))
            offs += len(ch) - overlap if (i < len(local_chunks) - 1) else len(ch)

    print(Fore.CYAN + "[3/3] Gerando embeddings e gravando índice FAISS..." + Style.RESET_ALL)
    encoder = SentenceTransformer(embedding_model)
    emb = encoder.encode(chunks, batch_size=64, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

    d = emb.shape[1]
    index = faiss.IndexFlatIP(d)  # Inner Product (com vetores normalizados ~ cos similarity)
    index.add(emb)

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)

    # salvar metadados e settings
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "w", encoding="utf-8") as f:
        for ch, m in zip(chunks, metadatas):
            rec = {
                "text": ch,
                "source": m.source,
                "chunk_id": m.chunk_id,
                "start_char": m.start_char,
                "end_char": m.end_char,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    settings = {
        "embedding_model": embedding_model,
        "dimension": int(d),
        "built_at": int(time.time()),
        "docs_path": os.path.abspath(docs_folder),
        "chunk_size": chunk_size,
        "overlap": overlap,
    }
    with open(os.path.join(os.path.dirname(index_path), "settings.json"), "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

    print(Fore.GREEN + f"OK: index salvo em {index_path}, meta em {meta_path}" + Style.RESET_ALL)


def load_meta(meta_path: str) -> List[Dict[str, Any]]:
    items = []
    with open(meta_path, "r", encoding="utf-8") as f:
        for line in f:
            items.append(json.loads(line))
    return items


def search_index(query: str, index_path: str, meta_path: str,
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 top_k: int = 5) -> List[Retrieved]:
    index = faiss.read_index(index_path)
    meta = load_meta(meta_path)

    encoder = SentenceTransformer(embedding_model)
    q = encoder.encode([query], convert_to_numpy=True, normalize_embeddings=True)

    scores, idxs = index.search(q, top_k)
    idxs = idxs[0]
    scores = scores[0]

    results: List[Retrieved] = []
    for i, s in zip(idxs, scores):
        if i == -1:
            continue
        rec = meta[i]
        m = Metadata(source=rec["source"], chunk_id=rec["chunk_id"], start_char=rec["start_char"], end_char=rec["end_char"])
        results.append(Retrieved(text=rec["text"], meta=m, score=float(s)))
    return results


# ================================
# Geradores
# ================================

class FlanT5Generator:
    def __init__(self, model_name: str = "google/flan-t5-base", device: Optional[str] = None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

    def generate(self, prompt: str, max_new_tokens: int = 256, temperature: float = 0.2, top_p: float = 0.9) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=temperature > 0,
                temperature=temperature,
                top_p=top_p,
            )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)


class TGIClientGenerator:
    """Cliente mínimo para Text Generation Inference (Hugging Face), endpoint /generate.
    Execute um servidor TGI local ou remoto (ex.: docker run ... ghcr.io/huggingface/text-generation-inference:latest \
        --model-id mistralai/Mistral-7B-Instruct-v0.3)
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, max_new_tokens: int = 256, temperature: float = 0.2, top_p: float = 0.9) -> str:
        url = f"{self.base_url}/generate"
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "do_sample": temperature > 0,
                "return_full_text": False,
            },
        }
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        # Resposta típica: {"generated_text": "..."} ou lista
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        return str(data)


# ================================
# RAG: montar prompt + fluxo pergunta -> recuperação -> geração
# ================================

def build_prompt(contexts: List[Retrieved], question: str, system_language: str = "pt") -> str:
    """Prompt simples instruindo o modelo a responder apenas com base no contexto."""
    lang_line = {
        "pt": (
            "Você é um assistente da ICTA Technology que responde APENAS com base no CONTEXTO abaixo. "
            "Se a resposta não estiver no contexto, diga educadamente que não sabe e sugira falar com um humano.\n"),
        "en": (
            "You are an ICTA Technology assistant. Answer ONLY using the CONTEXT below. "
            "If the answer is not in the context, say you don't know and suggest contacting a human.\n"),
    }.get(system_language, "pt")

    header = f"[INSTRUÇÕES]\n{lang_line}\n"
    ctx = "\n\n".join([f"[TRECHO {i+1} | score={c.score:.3f} | fonte={os.path.basename(c.meta.source)}]\n{c.text}" for i, c in enumerate(contexts)])
    q_line = f"\n\n[PERGUNTA]\n{question}\n\n[RESPOSTA]"
    return header + "[CONTEXTO]\n" + ctx + q_line


def answer_question(query: str, index_path: str, meta_path: str,
                    generator_type: str = "flan-t5",
                    model_name: str = "google/flan-t5-base",
                    tgi_url: Optional[str] = None,
                    top_k: int = 5,
                    max_new_tokens: int = 256,
                    system_language: str = "pt") -> Tuple[str, List[Retrieved]]:
    # Recuperação
    hits = search_index(query, index_path, meta_path, top_k=top_k)

    # Montar prompt
    prompt = build_prompt(hits, query, system_language=system_language)

    # Geração
    if generator_type == "flan-t5":
        gen = FlanT5Generator(model_name=model_name)
        out = gen.generate(prompt, max_new_tokens=max_new_tokens)
    elif generator_type == "tgi":
        if not tgi_url:
            raise ValueError("Para generator=tgi, especifique --tgi-url (ex.: http://localhost:8080)")
        gen = TGIClientGenerator(tgi_url)
        out = gen.generate(prompt, max_new_tokens=max_new_tokens)
    else:
        raise ValueError("generator inválido. Use 'flan-t5' ou 'tgi'.")

    return out.strip(), hits


# ================================
# Histórico
# ================================

def append_history(path: str, question: str, answer: str, retrieved: List[Retrieved]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rec = {
        "ts": int(time.time()),
        "question": question,
        "answer": answer,
        "retrieved": [
            {
                "source": r.meta.source,
                "chunk_id": r.meta.chunk_id,
                "score": r.score,
            }
            for r in retrieved
        ],
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ================================
# CLI
# ================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="RAG Chatbot (FAQ) — ICTA Technology")

    # Build index
    p.add_argument("--build-index", action="store_true", help="Construir índice FAISS a partir de --docs-path")
    p.add_argument("--docs-path", type=str, default="./data", help="Pasta com .txt")
    p.add_argument("--index-path", type=str, default="./index/faiss.index", help="Caminho para salvar/ler índice FAISS")
    p.add_argument("--meta-path", type=str, default="./index/meta.jsonl", help="Caminho para salvar/ler metadados")

    # Chat
    p.add_argument("--chat", action="store_true", help="Abrir loop de chat no terminal")
    p.add_argument("--generator", type=str, default="flan-t5", choices=["flan-t5", "tgi"], help="Motor de geração")
    p.add_argument("--model-name", type=str, default="google/flan-t5-base", help="Nome do modelo (para flan-t5)")
    p.add_argument("--tgi-url", type=str, default=None, help="URL do servidor TGI (ex.: http://localhost:8080)")
    p.add_argument("--top-k", type=int, default=5, help="Quantos trechos recuperar")
    p.add_argument("--max-new-tokens", type=int, default=256, help="Comprimento máximo da resposta gerada")
    p.add_argument("--system-language", type=str, default="pt", choices=["pt", "en"], help="Idioma do prompt")

    # História
    p.add_argument("--history-path", type=str, default="./history/chat_history.jsonl", help="Arquivo para registrar Q/A")

    # Index params
    p.add_argument("--chunk-size", type=int, default=800, help="Tamanho do chunk em caracteres")
    p.add_argument("--overlap", type=int, default=120, help="Sobreposição entre chunks")

    # (Bônus) LangChain — apenas uma flag explicativa
    p.add_argument("--use-langchain", action="store_true", help="(Opcional) Exemplo de execução com LangChain se instalado")

    return p.parse_args()


def run_chat(args: argparse.Namespace) -> None:
    # Modo sem LangChain (padrão)
    print(Fore.MAGENTA + "\n=== Chat ICTA (RAG) ===" + Style.RESET_ALL)
    print("Digite sua pergunta. Use /exit para sair, /show para ver os trechos recuperados mais recentes.\n")

    last_hits: List[Retrieved] = []
    while True:
        try:
            q = input(Fore.YELLOW + "Você: " + Style.RESET_ALL).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo...")
            break

        if not q:
            continue
        if q.lower() in {"/exit", ":q", "sair"}:
            print("Até mais!")
            break
        if q.lower() == "/show":
            if not last_hits:
                print("Nada recuperado ainda.")
                continue
            print(Fore.CYAN + "\nTrechos mais recentes:" + Style.RESET_ALL)
            for i, r in enumerate(last_hits, 1):
                print(f"[{i}] score={r.score:.3f} fonte={r.meta.source}#chunk{r.meta.chunk_id}")
                print(r.text[:500].replace("\n", " ") + ("..." if len(r.text) > 500 else ""))
                print("-")
            continue

        answer, hits = answer_question(
            q,
            index_path=args.index_path,
            meta_path=args.meta_path,
            generator_type=args.generator,
            model_name=args.model_name,
            tgi_url=args.tgi_url,
            top_k=args.top_k,
            max_new_tokens=args.max_new_tokens,
            system_language=args.system_language,
        )
        last_hits = hits

        print(Fore.GREEN + "Chatbot:" + Style.RESET_ALL, answer, "\n")
        try:
            append_history(args.history_path, q, answer, hits)
        except Exception as e:
            print(f"[WARN] Falha ao salvar histórico: {e}")


def main():
    args = parse_args()

    if args.build_index:
        build_faiss_index(
            docs_folder=args.docs_path,
            index_path=args.index_path,
            meta_path=args.meta_path,
            chunk_size=args.chunk_size,
            overlap=args.overlap,
        )
        return

    if args.chat:
        # Modo opcional com LangChain (se for realmente desejado)
        if args.use_langchain:
            try:
                from langchain_community.vectorstores import FAISS as LCFAISS
                from langchain_community.embeddings import HuggingFaceEmbeddings
                from langchain.llms import HuggingFacePipeline
                from transformers import pipeline

                print(Fore.BLUE + "[LangChain] Inicializando cadeia..." + Style.RESET_ALL)

                # Carregar índice FAISS existente para LangChain (reconstruindo a partir de meta + FAISS)
                # Simplesmente re-embedar com o mesmo modelo e reconstruir LCFAISS a partir do corpus.
                # (para reuso direto do .index seria necessário salvar também mapping; mantemos simples)
                meta = load_meta(args.meta_path)
                texts = [m["text"] for m in meta]
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                vectordb = LCFAISS.from_texts(texts, embeddings)

                # Gerador via pipeline (FLAN-T5)
                pipe = pipeline(
                    "text2text-generation",
                    model=args.model_name,
                    tokenizer=args.model_name,
                    max_new_tokens=args.max_new_tokens,
                )
                llm = HuggingFacePipeline(pipeline=pipe)

                from langchain.prompts import PromptTemplate
                from langchain.chains import RetrievalQA

                template = (
                    "Você é um assistente da ICTA Technology. Responda APENAS usando o contexto.\n"
                    "Se não houver resposta no contexto, diga que não sabe.\n\n"
                    "Contexto:\n{context}\n\nPergunta: {question}\nResposta:" )
                prompt = PromptTemplate(template=template, input_variables=["context", "question"])  # type: ignore

                qa = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=vectordb.as_retriever(search_kwargs={"k": args.top_k}),
                    chain_type_kwargs={"prompt": prompt},
                    return_source_documents=True,
                )

                print(Fore.MAGENTA + "\n=== Chat ICTA (RAG c/ LangChain) ===" + Style.RESET_ALL)
                print("Digite sua pergunta. /exit para sair.\n")
                while True:
                    try:
                        q = input(Fore.YELLOW + "Você: " + Style.RESET_ALL).strip()
                    except (EOFError, KeyboardInterrupt):
                        print("\nSaindo...")
                        break
                    if not q:
                        continue
                    if q.lower() in {"/exit", ":q", "sair"}:
                        print("Até mais!")
                        break
                    res = qa({"query": q})
                    ans = res.get("result", "(sem resposta)")
                    print(Fore.GREEN + "Chatbot:" + Style.RESET_ALL, ans, "\n")
            except Exception as e:
                print(Fore.RED + f"[LangChain] Erro: {e}\nVoltando ao modo padrão sem LangChain..." + Style.RESET_ALL)
                run_chat(args)
        else:
            run_chat(args)
        return

    # Se nenhum modo foi escolhido
    print("Nada a fazer. Use --build-index ou --chat. --help para ajuda.")


if __name__ == "__main__":
    main()
