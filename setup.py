#!/usr/bin/env python3
"""
Setup script para o RAG Chatbot ICTA Technology
"""

from setuptools import setup, find_packages
import os

# Lê o README para usar como descrição longa
def read_readme() -> str:
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "RAG Chatbot para FAQ - ICTA Technology"

# Lê os requirements
def read_requirements() -> list[str]:
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements: list[str] = []
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignora comentários e linhas vazias
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

if __name__ == "__main__":
    import sys
    
    # Se executado sem argumentos, mostra instruções de instalação
    if len(sys.argv) == 1:
        print("🚀 RAG Chatbot ICTA - Instruções de Instalação")
        print("=" * 50)
        print()
        print("Para instalar as dependências, execute um dos comandos:")
        print("1. pip install -r requirements.txt")
        print("2. python -m pip install -r requirements.txt")
        print()
        print("Para usar o chatbot após instalação:")
        print("python rag_chatbot_icta.py")
        print()
        print("Para instalação em modo desenvolvimento:")
        print("python setup.py develop")
        print()
        sys.exit(0)
    else:
        # Executa o setup normalmente com os argumentos fornecidos
        _ = setup(
        name="icta-rag-chatbot",
        version="1.0.0",
        author="ICTA Technology",
        author_email="jesse.fernandes@ictatechnology.com.br",
        description="RAG Chatbot para FAQ usando FAISS e modelos locais",
        long_description=read_readme(),
        long_description_content_type="text/markdown",
        url="https://github.com/jesseff20/rag-chatbot",
    
    # Configuração do pacote
    py_modules=["rag_chatbot_icta"],
    packages=find_packages(),
    
    # Dependências
    install_requires=read_requirements(),
    
    # Classificadores PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    
    # Requisitos de Python
    python_requires=">=3.8",
    
    # Scripts executáveis
    entry_points={
        "console_scripts": [
            "icta-rag=rag_chatbot_icta:main",
        ],
    },
    
    # Arquivos de dados incluídos
    package_data={
        "": ["data/*.txt", "README.md", "requirements.txt"],
    },
    include_package_data=True,
    
    # Palavras-chave para busca
    keywords="rag chatbot faq ai nlp machine-learning transformers faiss",
    
    # Dependências extras para desenvolvimento
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "langchain": [
            "langchain>=0.0.300",
            "langchain-community>=0.0.20",
        ],
    },
    
    # Metadados do projeto
    project_urls={
        "Bug Reports": "https://github.com/jesseff20/rag-chatbot/issues",
        "Source": "https://github.com/jesseff20/rag-chatbot",
        "Documentation": "https://github.com/jesseff20/rag-chatbot/blob/main/README.md",
        "Repository": "https://github.com/jesseff20/rag-chatbot.git",
    },
    )
