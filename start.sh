#!/bin/bash

# Script de inicialização do Data Modeling App

set -e

echo "🗄️  Data Modeling App - Databricks"
echo "=================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "Instale Python 3.9 ou superior"
    exit 1
fi

echo "✅ Python: $(python3 --version)"
echo ""

# Verificar se está em um virtualenv
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Não está em um ambiente virtual"
    echo ""
    read -p "Deseja criar um ambiente virtual? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 Criando ambiente virtual..."
        python3 -m venv venv
        echo "✅ Ambiente virtual criado!"
        echo ""
        echo "Execute:"
        echo "  source venv/bin/activate  # Linux/Mac"
        echo "  venv\\Scripts\\activate     # Windows"
        echo ""
        echo "Depois execute este script novamente."
        exit 0
    fi
fi

# Instalar dependências
echo "📦 Verificando dependências..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Instalando dependências..."
    pip install -r requirements.txt
    echo "✅ Dependências instaladas!"
else
    echo "✅ Dependências já instaladas"
fi
echo ""

# Executar testes
echo "🧪 Executando testes..."
if python3 test_app.py; then
    echo "✅ Todos os testes passaram!"
else
    echo "❌ Alguns testes falharam"
    read -p "Deseja continuar mesmo assim? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# Limpar terminal
clear

echo "🚀 Iniciando Data Modeling App..."
echo ""
echo "O app abrirá no navegador em alguns segundos..."
echo ""
echo "📚 Dicas:"
echo "  - Pressione Ctrl+C para parar o app"
echo "  - Acesse: http://localhost:8501"
echo "  - Leia QUICKSTART.md para começar"
echo ""
echo "=================================="
echo ""

# Iniciar Streamlit
streamlit run app.py

