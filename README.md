# 🗄️ Data Modeling App - Databricks

Aplicação para modelagem de dados visual no-code usando **Streamlit Native Theming** com tema dark inspirado no **Spotify**.

## 🎨 Theming

A aplicação utiliza o sistema nativo de theming do Streamlit (v1.30+) conforme a [documentação oficial](https://docs.streamlit.io/develop/concepts/configuration/theming).

### Tema Dark Spotify

As cores foram inspiradas no design system do Spotify:

- **Primary Color**: `#1DB954` (Spotify Green)
- **Background**: `#121212` (Spotify Dark)
- **Secondary Background**: `#181818` (Spotify Lighter Dark)
- **Text Color**: `#FFFFFF` (White)
- **Sidebar Background**: `#000000` (Pure Black)

## 📁 Estrutura do Projeto

```
data-modeling/
├── .streamlit/
│   └── config.toml          # Configuração de tema Streamlit
├── app.py                   # Aplicação principal (simplificada)
├── models.py                # Modelos de dados
├── diagram_renderer.py      # Renderização de diagramas (Mermaid ERD)
├── sql_generator.py         # Geração de SQL DDL
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🚀 Como executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

## ✨ Funcionalidades

### ➕ Criar
- **Criar Tabelas**: Adicione tabelas com nome e descrição
- **Adicionar Campos**: Defina campos com:
  - Nome e tipo de dado
  - Descrição
  - Chave primária (PK) / Chave estrangeira (FK)
  - Tags personalizadas
- **Relacionamentos**: Crie relacionamentos entre tabelas
  - 1:1 (One to One)
  - 1:N (One to Many)
  - N:1 (Many to One)
  - N:N (Many to Many)

### 💾 Salvar/Carregar
- **Exportar JSON**: Salve o modelo completo em formato JSON
- **Importar JSON**: Carregue modelos salvos anteriormente
- **Gerar SQL DDL**: Gere scripts SQL para criar as tabelas no Databricks SQL

### ⚙️ Configurações
- **Zoom**: Ajuste o nível de zoom do diagrama (0.5x a 2.0x)
- **Centralizar**: Centralize o diagrama na tela
- **Limpar Modelo**: Remova todas as tabelas e relacionamentos

### 📊 Diagrama ERD (Entity Relationship Diagram)
- **Visualização profissional**: Diagrama ERD padrão usando Mermaid
- **Formato padrão**: Sintaxe Mermaid reconhecida universalmente
- **Campos visíveis**: Todos os campos e constraints mostrados
- **Relacionamentos claros**: Símbolos padrão (|o--o|, |o--o{, etc.)
- **Labels informativos**: Tipo de relação e campos relacionados
- **Exportável**: Código Mermaid pode ser usado em documentação
- **Controles de Zoom**: Botões +/- e reset no canto inferior direito
- **Zoom com Mouse**: Ctrl + scroll para zoom suave
- **Tamanho Otimizado**: Inicia em 60% para melhor visualização

## 🎯 Diferenças da versão anterior

### ❌ Removido
- ~~Bootstrap CSS e componentes~~
- ~~Font Awesome icons~~
- ~~CSS customizado extensivo~~
- ~~JavaScript personalizado para ícones~~
- ~~Theming manual com CSS variables~~

### ✅ Novo
- **Streamlit Native Theming**: Sistema oficial de temas
- **Configuração via .streamlit/config.toml**: Fácil customização
- **Código simplificado**: ~500 linhas vs ~2000 linhas
- **Melhor performance**: Menos CSS/JS para processar
- **Spotify Theme**: Design moderno e profissional
- **Cores consistentes**: Paleta unificada em toda a app

## 🎨 Customização do Tema

Para customizar o tema, edite o arquivo `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1DB954"        # Cor primária (botões, highlights)
backgroundColor = "#121212"      # Fundo principal
secondaryBackgroundColor = "#181818"  # Fundo secundário
textColor = "#FFFFFF"           # Cor do texto
font = "sans serif"             # Fonte

[theme.dark.sidebar]
backgroundColor = "#000000"      # Fundo da sidebar
```

Referência completa: https://docs.streamlit.io/develop/concepts/configuration/theming

## 📦 Dependências

- `streamlit >= 1.30.0` - Framework web (com components.html para Mermaid)
- `pandas` - Manipulação de dados
- Mermaid.js via CDN (carregado automaticamente)

## 🔧 Desenvolvimento

### Estrutura de dados

**DataModel**: Modelo completo
- `tables`: Dict[str, Table]
- `relationships`: List[Relationship]

**Table**: Tabela individual
- `name`: Nome da tabela
- `description`: Descrição opcional
- `fields`: List[Field]
- `position_x`, `position_y`: Posição no diagrama

**Field**: Campo de tabela
- `name`: Nome do campo
- `data_type`: Tipo de dado SQL
- `description`: Descrição opcional
- `is_primary_key`: Booleano
- `is_foreign_key`: Booleano
- `is_nullable`: Booleano (default: True)
- `tags`: List[str]

**Relationship**: Relacionamento entre tabelas
- `from_table`: Tabela origem
- `to_table`: Tabela destino
- `relationship_type`: RelationshipType enum

## 📝 Licença

Este projeto é parte do ecossistema Databricks Apps.

## 🤝 Contribuindo

Para contribuir:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📚 Referências

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Theming](https://docs.streamlit.io/develop/concepts/configuration/theming)
- [Databricks Apps](https://docs.databricks.com/dev-tools/databricks-apps/)
- [Spotify Design System](https://developer.spotify.com/documentation/general/design-and-branding/)

---

**Versão**: 2.0 (Streamlit Native Theming)  
**Última atualização**: Dezembro 2025
