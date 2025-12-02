# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o Data Modeling App! 🎉

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Posso Contribuir?](#como-posso-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Processo de Contribuição](#processo-de-contribuição)
- [Padrões de Código](#padrões-de-código)
- [Processo de Review](#processo-de-review)

## 📜 Código de Conduta

Este projeto segue o [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).
Ao participar, você concorda em seguir suas diretrizes.

### Nossos Valores

- **Respeito**: Trate todos com respeito e empatia
- **Colaboração**: Trabalhe junto para melhorar o projeto
- **Qualidade**: Mantenha altos padrões de código
- **Transparência**: Comunique-se abertamente

## 🚀 Como Posso Contribuir?

### 🐛 Reportar Bugs

Encontrou um bug? Ajude-nos a corrigi-lo!

1. Verifique se o bug já não foi reportado nas [Issues](https://github.com/seu-repo/issues)
2. Crie uma nova issue com:
   - **Título claro**: "Bug: [descrição curta]"
   - **Descrição detalhada**: O que aconteceu vs. o esperado
   - **Passos para reproduzir**: Lista numerada
   - **Ambiente**: OS, Python version, Databricks version
   - **Screenshots**: Se aplicável

### 💡 Sugerir Funcionalidades

Tem uma ideia para melhorar o app?

1. Verifique se já não foi sugerida
2. Crie uma issue com:
   - **Título**: "Feature: [descrição]"
   - **Motivação**: Por que é útil?
   - **Descrição**: Como funcionaria?
   - **Exemplos**: Casos de uso

### 🔧 Contribuir com Código

Quer implementar uma funcionalidade ou correção?

1. Escolha uma issue existente ou crie uma nova
2. Comente na issue que está trabalhando nisso
3. Siga o [Processo de Contribuição](#processo-de-contribuição)

### 📚 Melhorar Documentação

Documentação sempre pode ser melhorada!

- Corrigir typos
- Adicionar exemplos
- Clarificar instruções
- Traduzir documentos

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.9+
- Git
- IDE recomendado: VS Code ou PyCharm

### Setup

```bash
# Clone o repositório
git clone https://github.com/seu-repo/data-modeling.git
cd data-modeling

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Instale dependências de desenvolvimento (opcional)
pip install -r requirements-dev.txt

# Execute os testes
python3 test_app.py

# Execute o app localmente
streamlit run app.py
```

## 🔄 Processo de Contribuição

### 1. Fork e Clone

```bash
# Fork no GitHub (botão Fork)
# Clone seu fork
git clone https://github.com/seu-usuario/data-modeling.git
cd data-modeling

# Adicione o repositório original como upstream
git remote add upstream https://github.com/repo-original/data-modeling.git
```

### 2. Crie uma Branch

```bash
# Atualize seu main
git checkout main
git pull upstream main

# Crie uma branch descritiva
git checkout -b feature/nome-da-funcionalidade
# ou
git checkout -b bugfix/descricao-do-bug
```

**Convenção de nomes:**
- `feature/` - Nova funcionalidade
- `bugfix/` - Correção de bug
- `docs/` - Alterações na documentação
- `refactor/` - Refatoração de código
- `test/` - Adição de testes

### 3. Faça suas Alterações

```bash
# Edite os arquivos necessários
# ...

# Adicione os arquivos alterados
git add .

# Commit com mensagem descritiva
git commit -m "feat: adiciona export para PNG"
```

### 4. Escreva Testes

Se adicionar funcionalidade nova, adicione testes em `test_app.py`:

```python
def test_nova_funcionalidade():
    """Testa a nova funcionalidade"""
    # Arrange
    model = DataModel()
    
    # Act
    resultado = model.nova_funcionalidade()
    
    # Assert
    assert resultado is not None
    print("✅ test_nova_funcionalidade passou!")
```

Execute os testes:

```bash
python3 test_app.py
```

### 5. Atualize a Documentação

- Atualize README.md se necessário
- Adicione entrada no CHANGELOG.md
- Adicione docstrings no código
- Atualize exemplos se aplicável

### 6. Push e Pull Request

```bash
# Push para seu fork
git push origin feature/nome-da-funcionalidade
```

No GitHub:
1. Vá para seu fork
2. Clique em "Compare & pull request"
3. Preencha o template do PR
4. Aguarde review

## 📝 Padrões de Código

### Python Style Guide

Seguimos [PEP 8](https://pep8.org/):

```python
# Bom ✅
def calculate_total(items: List[Item]) -> float:
    """
    Calcula o total de uma lista de itens.
    
    Args:
        items: Lista de itens para calcular
        
    Returns:
        Valor total como float
    """
    return sum(item.price for item in items)

# Ruim ❌
def calc(i):
    return sum(x.p for x in i)
```

### Convenções

**Naming:**
- `snake_case` para funções e variáveis
- `PascalCase` para classes
- `UPPER_CASE` para constantes

**Imports:**
```python
# Standard library
import json
from datetime import datetime

# Third-party
import streamlit as st
import pandas as pd

# Local
from models import DataModel
from sql_generator import generate_ddl
```

**Docstrings:**
```python
def funcao(parametro: str) -> bool:
    """
    Breve descrição da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        parametro: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
        
    Raises:
        ValueError: Quando parametro é inválido
    """
    pass
```

### Type Hints

Use type hints sempre que possível:

```python
from typing import List, Dict, Optional

def process_table(
    table: Table,
    options: Optional[Dict[str, Any]] = None
) -> List[Field]:
    """Process table with options."""
    pass
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python3 test_app.py

# Com coverage (se instalado)
pytest --cov=. test_app.py
```

### Escrever Testes

```python
def test_minha_funcao():
    """Testa minha funcao."""
    # Arrange - Setup
    input_data = "test"
    
    # Act - Executar
    result = minha_funcao(input_data)
    
    # Assert - Verificar
    assert result == "expected"
    print("✅ test_minha_funcao passou!")
```

## 🔍 Processo de Review

### O que Avaliamos

1. **Funcionalidade**: Código funciona conforme esperado?
2. **Testes**: Testes adequados incluídos?
3. **Documentação**: Alterações documentadas?
4. **Estilo**: Segue padrões do projeto?
5. **Performance**: Sem regressões de performance?

### Checklist do PR

Antes de submeter, verifique:

- [ ] Código funciona localmente
- [ ] Testes passando
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado
- [ ] Sem erros de linting
- [ ] Commit messages descritivos
- [ ] PR description completo

### Respondendo a Feedback

- Seja receptivo a sugestões
- Faça perguntas se não entender
- Atualize o PR conforme necessário
- Marque conversas como resolvidas

## 📊 Commit Messages

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, espaços, etc.
- `refactor`: Refatoração de código
- `test`: Adição de testes
- `chore`: Manutenção

**Exemplos:**

```bash
feat(sql): adiciona suporte para views
fix(diagram): corrige posicionamento de tabelas
docs(readme): atualiza instruções de instalação
refactor(models): simplifica estrutura de Field
test(sql): adiciona testes para geração DDL
```

## 🎨 Assets e Design

### Adicionando Assets

- Coloque imagens em `assets/images/`
- Mantenha tamanhos razoáveis (< 500KB)
- Use formatos web-friendly (PNG, JPG, SVG)

### UI/UX Guidelines

- Mantenha consistência com design existente
- Use cores da paleta Databricks
- Teste em diferentes tamanhos de tela
- Considere acessibilidade

## 🌟 Primeiros Passos

Novo no projeto? Comece com issues marcadas como:
- `good first issue`
- `help wanted`
- `documentation`

## 💬 Comunicação

- **Issues**: Para bugs e features
- **Discussions**: Para perguntas gerais
- **PR Comments**: Para discussões sobre código

## 🙏 Reconhecimento

Todos os contribuidores serão listados no README.md!

## ❓ Dúvidas?

Não hesite em:
- Abrir uma issue com sua pergunta
- Comentar em PRs existentes
- Entrar em contato com mantenedores

---

**Obrigado por contribuir! Sua ajuda torna este projeto melhor para todos.** 🚀

