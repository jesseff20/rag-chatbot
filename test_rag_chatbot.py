#!/usr/bin/env python3
"""
Testes básicos para o RAG Chatbot ICTA
"""

import pytest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Adiciona o diretório do projeto ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import rag_chatbot_icta
except ImportError:
    pytest.skip("Módulo rag_chatbot_icta não encontrado", allow_module_level=True)


class TestRAGChatbot:
    """Testes básicos para verificar funcionalidades do chatbot"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, "data")
        self.index_dir = os.path.join(self.temp_dir, "index")
        os.makedirs(self.data_dir)
        os.makedirs(self.index_dir)
        
        # Cria um arquivo de texto de exemplo
        self.test_file = os.path.join(self.data_dir, "test.txt")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Este é um texto de teste para o chatbot RAG do ICTA Technology.")
    
    def teardown_method(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_read_text_files(self):
        """Testa a função de leitura de arquivos de texto"""
        data = rag_chatbot_icta.read_text_files(self.data_dir)
        assert len(data) == 1
        assert self.test_file in data
        assert "ICTA Technology" in data[self.test_file]
    
    def test_chunk_text(self):
        """Testa a função de quebra de texto em chunks"""
        text = "Este é um texto de exemplo que será quebrado em pedaços menores para testar a funcionalidade."
        chunks = rag_chatbot_icta.chunk_text(text, chunk_size=50, overlap=10)
        assert len(chunks) > 1
        assert all(len(chunk) <= 50 for chunk in chunks)
    
    def test_imports(self):
        """Testa se todas as dependências necessárias podem ser importadas"""
        try:
            import faiss
            import numpy as np
            import tqdm
            import colorama
            import sentence_transformers
            import transformers
            import torch
            import requests
            assert True  # Se chegou aqui, todas as importações funcionaram
        except ImportError as e:
            pytest.fail(f"Falha ao importar dependência: {e}")


class TestProjectStructure:
    """Testes para verificar a estrutura do projeto"""
    
    def test_required_files_exist(self):
        """Verifica se os arquivos necessários existem"""
        project_root = os.path.dirname(os.path.abspath(__file__))
        
        required_files = [
            "rag_chatbot_icta.py",
            "requirements.txt",
            "setup.py",
            "README.md"
        ]
        
        for file_name in required_files:
            file_path = os.path.join(project_root, file_name)
            assert os.path.exists(file_path), f"Arquivo obrigatório não encontrado: {file_name}"
    
    def test_data_directory_exists(self):
        """Verifica se o diretório de dados existe"""
        project_root = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(project_root, "data")
        assert os.path.exists(data_dir), "Diretório 'data' não encontrado"
        
        # Verifica se há pelo menos um arquivo .txt
        txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
        assert len(txt_files) > 0, "Nenhum arquivo .txt encontrado no diretório 'data'"


def test_requirements_file():
    """Testa se o arquivo requirements.txt está bem formado"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(project_root, "requirements.txt")
    
    with open(requirements_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Verifica se contém as dependências principais
    requirements_text = ''.join(lines)
    essential_packages = [
        'faiss-cpu',
        'sentence-transformers',
        'transformers',
        'torch',
        'numpy',
        'tqdm',
        'colorama',
        'requests'
    ]
    
    for package in essential_packages:
        assert package in requirements_text, f"Pacote essencial '{package}' não encontrado em requirements.txt"


if __name__ == "__main__":
    # Executa os testes se o arquivo for executado diretamente
    pytest.main([__file__, "-v"])
