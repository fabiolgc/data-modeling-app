.PHONY: help install install-dev run test clean lint format deploy

# Variáveis
PYTHON := python3
PIP := $(PYTHON) -m pip
STREAMLIT := streamlit
APP_NAME := data-modeling

help: ## Mostra esta mensagem de ajuda
	@echo "🗄️  Data Modeling App - Makefile"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências de produção
	@echo "📦 Instalando dependências..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependências instaladas!"

install-dev: ## Instala dependências de desenvolvimento
	@echo "📦 Instalando dependências de desenvolvimento..."
	$(PIP) install -r requirements-dev.txt
	@echo "✅ Dependências de dev instaladas!"

run: ## Executa o app localmente
	@echo "🚀 Iniciando Data Modeling App..."
	$(STREAMLIT) run app.py

test: ## Executa os testes
	@echo "🧪 Executando testes..."
	$(PYTHON) test_app.py

test-coverage: ## Executa testes com coverage
	@echo "🧪 Executando testes com coverage..."
	pytest --cov=. --cov-report=html test_app.py
	@echo "📊 Report gerado em htmlcov/index.html"

lint: ## Verifica code quality
	@echo "🔍 Verificando code quality..."
	flake8 *.py --max-line-length=100
	pylint *.py --max-line-length=100
	@echo "✅ Lint completo!"

format: ## Formata o código
	@echo "🎨 Formatando código..."
	black *.py
	isort *.py
	@echo "✅ Código formatado!"

type-check: ## Verifica tipos
	@echo "🔎 Verificando tipos..."
	mypy *.py
	@echo "✅ Type checking completo!"

clean: ## Limpa arquivos temporários
	@echo "🧹 Limpando arquivos temporários..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Limpeza concluída!"

deploy: ## Deploy no Databricks
	@echo "🚀 Fazendo deploy no Databricks..."
	@if command -v databricks >/dev/null 2>&1; then \
		databricks apps deploy $(APP_NAME); \
		echo "✅ Deploy concluído!"; \
	else \
		echo "❌ Databricks CLI não encontrado!"; \
		echo "Instale com: pip install databricks-cli"; \
		exit 1; \
	fi

deploy-check: ## Verifica status do deploy
	@echo "🔍 Verificando status do app..."
	databricks apps get $(APP_NAME)

logs: ## Mostra logs do app
	@echo "📋 Logs do app:"
	databricks apps logs $(APP_NAME) --follow

validate: ## Valida configuração do app
	@echo "✅ Validando configuração..."
	@if [ -f "app.yaml" ]; then \
		echo "✅ app.yaml existe"; \
	else \
		echo "❌ app.yaml não encontrado!"; \
		exit 1; \
	fi
	@if [ -f "requirements.txt" ]; then \
		echo "✅ requirements.txt existe"; \
	else \
		echo "❌ requirements.txt não encontrado!"; \
		exit 1; \
	fi
	@if [ -f "app.py" ]; then \
		echo "✅ app.py existe"; \
	else \
		echo "❌ app.py não encontrado!"; \
		exit 1; \
	fi
	@echo "✅ Validação completa!"

check-all: validate test lint ## Executa todas as verificações
	@echo "✅ Todas as verificações passaram!"

dev-setup: install-dev ## Setup completo para desenvolvimento
	@echo "🔧 Configurando ambiente de desenvolvimento..."
	@if [ ! -d "venv" ]; then \
		echo "Criando ambiente virtual..."; \
		$(PYTHON) -m venv venv; \
		echo "✅ Ambiente virtual criado!"; \
		echo "Execute: source venv/bin/activate"; \
	else \
		echo "✅ Ambiente virtual já existe"; \
	fi

version: ## Mostra versões instaladas
	@echo "📌 Versões:"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Streamlit: $$($(STREAMLIT) --version)"
	@if command -v databricks >/dev/null 2>&1; then \
		echo "Databricks CLI: $$(databricks --version)"; \
	fi

example: ## Carrega exemplo de e-commerce
	@echo "📦 Modelo de exemplo disponível em:"
	@echo "examples/ecommerce_model.json"
	@echo ""
	@echo "Para importar:"
	@echo "1. Execute o app: make run"
	@echo "2. Vá para: Salvar/Carregar > Importar Modelo"
	@echo "3. Faça upload do arquivo: examples/ecommerce_model.json"

docs: ## Abre a documentação
	@echo "📚 Documentação:"
	@echo "- README.md - Documentação principal"
	@echo "- QUICKSTART.md - Início rápido"
	@echo "- DEPLOYMENT.md - Guia de deploy"
	@echo "- CONTRIBUTING.md - Como contribuir"

tree: ## Mostra estrutura do projeto
	@echo "📁 Estrutura do projeto:"
	@tree -I '__pycache__|*.pyc|venv|.git' -L 2 || \
	find . -maxdepth 2 -not -path '*/\.*' -not -path '*/__pycache__/*' -not -path '*/venv/*' | sort

# Comandos de atalho
r: run ## Atalho para run
t: test ## Atalho para test
c: clean ## Atalho para clean
d: deploy ## Atalho para deploy

