#!/usr/bin/env python3
"""
Script de instalação e configuração automática para o RAG Chatbot ICTA
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step_num: int, description: str) -> None:
    """Imprime uma etapa numerada com formatação"""
    print(f"\n🔄 Passo {step_num}: {description}")
    print("=" * 50)

def print_substep(description: str) -> None:
    """Imprime uma sub-etapa com indentação"""
    print(f"   🔹 {description}")

def run_command(command: str, description: str) -> bool:
    """Executa um comando e mostra o resultado"""
    print(f"Executando: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Sucesso!")
        if result.stdout:
            print("Saída:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Erro!")
        print("Código de erro:", e.returncode)
        if e.stderr:
            print("Erro:", e.stderr)
        return False

def check_python_version():
    """Verifica a versão do Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Erro: Python 3.8+ é necessário")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} encontrado")
    return True

def install_requirements() -> bool:
    """Instala as dependências do requirements.txt"""
    print_substep("Verificando arquivo requirements.txt...")
    if not os.path.exists("requirements.txt"):
        print("❌ Arquivo requirements.txt não encontrado")
        return False
    
    print_substep("Instalando pacotes essenciais...")
    print("   📦 faiss-cpu - Busca vetorial de alta performance")
    print("   📦 sentence-transformers - Embeddings de texto")
    print("   📦 transformers - Modelos de linguagem da Hugging Face")
    print("   📦 torch - Framework de deep learning")
    print("   📦 numpy - Computação numérica")
    print("   📦 tqdm - Barras de progresso")
    print("   📦 colorama - Cores no terminal")
    print("   📦 requests - Cliente HTTP")
    
    return run_command("pip install -r requirements.txt", "Instalando dependências")

def test_installation() -> bool:
    """Testa se a instalação foi bem-sucedida"""
    print_substep("Testando importações críticas...")
    
    test_imports = [
        ("numpy", "numpy", "Computação numérica fundamental"),
        ("faiss", "faiss-cpu", "Índice vetorial FAISS para busca semântica"),
        ("sentence_transformers", "sentence-transformers", "Modelos de embeddings"),
        ("transformers", "transformers", "Biblioteca Transformers da Hugging Face"),
        ("torch", "torch", "PyTorch para deep learning"),
        ("tqdm", "tqdm", "Barras de progresso"),
        ("colorama", "colorama", "Cores no terminal"),
        ("requests", "requests", "Cliente HTTP para APIs")
    ]
    
    failed_imports: list[str] = []
    for module, package, description in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Falha ao importar: {', '.join(failed_imports)}")
        print("💡 Tente reinstalar: pip install -r requirements.txt")
        return False
    
    print("\n✅ Todas as dependências foram instaladas com sucesso!")
    return True

def setup_directories() -> None:
    """Configura os diretórios necessários"""
    print_substep("Criando estrutura de diretórios...")
    directories = [
        ("data", "Armazena arquivos .txt com FAQs e documentos"),
        ("index", "Contém índices FAISS e metadados gerados"),
        ("history", "Histórico de conversas em formato JSONL")
    ]
    
    for dir_name, description in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"   ✅ '{dir_name}/' criado - {description}")
        else:
            print(f"   ✅ '{dir_name}/' já existe - {description}")
    
    # Criar README nos diretórios se não existirem
    print_substep("Configurando arquivos de documentação...")
    readme_files = {
        "index/README.txt": "Este diretório contém os índices FAISS gerados automaticamente.\nExecute: python rag_chatbot_icta.py --build-index",
        "history/README.txt": "Este diretório contém o histórico de conversas em formato JSONL.\nGerado automaticamente durante o uso do chat."
    }
    
    for file_path, content in readme_files.items():
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                _ = f.write(content)
            print(f"   ✅ '{file_path}' criado")
        else:
            print(f"   ✅ '{file_path}' já existe")

def run_basic_test() -> bool:
    """Executa um teste básico do sistema"""
    print_substep("Executando verificações do sistema...")
    
    # Verifica se o arquivo principal existe
    if not os.path.exists("rag_chatbot_icta.py"):
        print("   ❌ Arquivo rag_chatbot_icta.py não encontrado")
        return False
    print("   ✅ Arquivo principal encontrado")
    
    # Tenta importar o módulo principal
    try:
        print_substep("Testando importação do módulo principal...")
        import rag_chatbot_icta
        print("   ✅ Módulo principal importado com sucesso")
        
        # Testa função básica
        if hasattr(rag_chatbot_icta, 'chunk_text'):
            print_substep("Testando funcionalidade de divisão de texto...")
            test_text = "Este é um teste básico da funcionalidade de chunking do RAG."
            chunks = rag_chatbot_icta.chunk_text(test_text, chunk_size=25, overlap=5)
            if len(chunks) > 0:
                print(f"   ✅ Função chunk_text funcionando ({len(chunks)} chunks gerados)")
            else:
                print("   ❌ Função chunk_text retornou lista vazia")
                return False
        
        # Verifica outras funções essenciais
        required_functions = ['read_text_files', 'build_faiss_index']
        for func_name in required_functions:
            if hasattr(rag_chatbot_icta, func_name):
                print(f"   ✅ Função '{func_name}' disponível")
            else:
                print(f"   ⚠️ Função '{func_name}' não encontrada")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro ao importar módulo: {e}")
        return False

def main() -> None:
    """Função principal de instalação"""
    print("🚀 Instalador Automático - RAG Chatbot ICTA Technology")
    print("=" * 60)
    print("📋 Este script irá:")
    print("   • Verificar a versão do Python (>=3.8)")
    print("   • Instalar todas as dependências necessárias")
    print("   • Configurar a estrutura de diretórios")
    print("   • Executar testes básicos do sistema")
    print("   • Preparar o ambiente para uso")
    
    # Passo 1: Verificar Python
    print_step(1, "Verificando versão do Python")
    print_substep("Verificando compatibilidade...")
    if not check_python_version():
        print("\n❌ INSTALAÇÃO CANCELADA")
        print("💡 Instale Python 3.8 ou superior e tente novamente")
        sys.exit(1)
    
    # Passo 2: Instalar dependências
    print_step(2, "Instalando dependências do projeto")
    if not install_requirements():
        print("\n❌ FALHA NA INSTALAÇÃO DAS DEPENDÊNCIAS")
        print("💡 Comandos para debug:")
        print("   pip install --upgrade pip")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Passo 3: Testar instalação
    print_step(3, "Validando instalação das dependências")
    if not test_installation():
        print("\n❌ TESTE DE INSTALAÇÃO FALHOU")
        print("💡 Algumas dependências podem não ter sido instaladas corretamente")
        sys.exit(1)
    
    # Passo 4: Configurar diretórios
    print_step(4, "Configurando estrutura do projeto")
    setup_directories()
    
    # Passo 5: Teste básico do sistema
    print_step(5, "Executando testes básicos do sistema")
    if not run_basic_test():
        print("\n⚠️ TESTE BÁSICO FALHOU")
        print("💡 A instalação pode estar ok, mas algumas funcionalidades podem não funcionar")
        print("💡 Verifique o arquivo rag_chatbot_icta.py")
    
    # Finalização
    print("\n" + "=" * 60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📋 Estrutura do projeto configurada:")
    print("   📁 data/     - Coloque seus arquivos .txt aqui")
    print("   📁 index/    - Índices FAISS (gerados automaticamente)")
    print("   📁 history/  - Histórico de conversas")
    print("\n🚀 Próximos passos:")
    print("   1️⃣ Adicione seus arquivos .txt no diretório 'data/'")
    print("   2️⃣ Construa o índice:")
    print("      python rag_chatbot_icta.py --build-index")
    print("   3️⃣ Inicie o chat:")
    print("      python rag_chatbot_icta.py --chat")
    print("\n📖 Documentação:")
    print("   • README.md - Guia completo de uso")
    print("   • COMANDOS.md - Comandos rápidos")
    print("   • https://github.com/jesseff20/rag-chatbot")
    print("\n💡 Dicas:")
    print("   • Execute 'python rag_chatbot_icta.py --help' para ver todas as opções")
    print("   • Use 'python -m pytest test_rag_chatbot.py' para executar testes")
    print("   • Para modelos maiores, use 'google/flan-t5-large'")

if __name__ == "__main__":
    main()
