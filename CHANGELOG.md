# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [2.1.0] - 2025-12-03

### 🎨 Mudança: Migração para Mermaid ERD

#### Adicionado
- **Mermaid ERD**: Substituído `streamlit-agraph` por `streamlit-mermaid`
- **Diagramas padrão**: ERD (Entity Relationship Diagram) com sintaxe Mermaid
- **Campos nos relacionamentos**: Labels mostram os campos relacionados (ex: `id:cliente_id`)
- **Seletor de campos**: UI para especificar quais campos se relacionam
- **Sintaxe universal**: Código Mermaid pode ser usado em docs, GitHub, etc.

#### Modificado
- ✏️ **diagram_renderer.py**: Reescrito para gerar sintaxe Mermaid ERD
- ✏️ **app.py**: Seleção de tabela via selectbox ao invés de clique
- ✏️ **requirements.txt**: `streamlit-mermaid` ao invés de `streamlit-agraph`
- ✏️ **Configurações**: Removido zoom (não aplicável em Mermaid)

#### Removido
- ❌ `streamlit-agraph` e dependências
- ❌ Interatividade de arrastar e zoom
- ❌ Controles manuais de posição de nós

### 📊 Vantagens do Mermaid

| Aspecto | agraph (v1.x) | Mermaid (v2.1) |
|---------|---------------|----------------|
| Tipo de diagrama | Grafo genérico | ERD padrão |
| Sintaxe | Python Node/Edge | Mermaid text |
| Campos na tabela | Texto formatado | ERD nativo |
| Relacionamentos | Linhas customizadas | Símbolos padrão |
| Exportar | JSON | Mermaid code |
| Documentação | Limitada | GitHub, GitLab, docs |

## [2.0.0] - 2025-12-02

### 🎨 Mudança Major: Migração para Streamlit Native Theming

#### Adicionado
- **Streamlit Native Theming**: Sistema oficial de temas do Streamlit
- **Arquivo `.streamlit/config.toml`**: Configuração centralizada de tema
- **Tema Dark Spotify**: Paleta de cores inspirada no Spotify
  - Primary Color: `#1DB954` (Spotify Green)
  - Background: `#121212` (Spotify Dark)
  - Sidebar: `#000000` (Pure Black)
- **Código simplificado**: Aplicação reduzida de ~2000 para ~500 linhas
- **README atualizado**: Documentação completa do novo sistema
- **CHANGELOG.md**: Este arquivo

#### Removido
- ❌ Bootstrap CSS e todos os componentes Bootstrap
- ❌ Font Awesome icons e CDN links
- ❌ ~1500 linhas de CSS customizado
- ❌ JavaScript personalizado para injeção de ícones
- ❌ CSS variables customizadas (`--db-coral`, `--db-bg-primary`, etc.)
- ❌ Funções auxiliares `create_badge()` e `create_alert()`
- ❌ Sistema de navegação customizado com botões
- ❌ Tooltips customizados
- ❌ Feature "Enter to Apply"

#### Modificado
- ✏️ **app.py**: Reescrito do zero usando componentes nativos
  - Navegação agora usa `st.radio()` ao invés de botões customizados
  - Layout simplificado com componentes nativos
  - Remoção de HTML/CSS customizado
  - CSS mínimo apenas para ajustes finos
- ✏️ **diagram_renderer.py**: Cores atualizadas para tema Spotify
  - Relacionamentos: Tons de verde do Spotify
  - Nós (tabelas): Fundo `#282828` com borda `#535353`
  - Nó selecionado: `#1DB954` (Spotify Green)
  - Background do grafo: `#121212` (Spotify Dark)
  - Highlight color: `#1DB954`
  - Labels dos edges: Texto branco em fundo escuro

### 📊 Comparação

| Aspecto | Versão 1.x (Bootstrap) | Versão 2.0 (Native) |
|---------|------------------------|---------------------|
| Linhas de código | ~2000 | ~500 |
| CSS customizado | ~1500 linhas | ~20 linhas |
| JavaScript | ~300 linhas | 0 linhas |
| Dependências externas | Bootstrap + Font Awesome | Nenhuma |
| Configuração | CSS inline | `.streamlit/config.toml` |
| Performance | Moderada | Excelente |
| Manutenibilidade | Complexa | Simples |
| Customização | Via CSS | Via TOML |

### 🎯 Benefícios da Migração

1. **Simplicidade**: Código 75% menor e mais legível
2. **Performance**: Menos CSS/JS para processar
3. **Manutenção**: Configuração centralizada em arquivo TOML
4. **Consistência**: Usa componentes nativos do Streamlit
5. **Documentação**: Segue padrões oficiais do Streamlit
6. **Escalabilidade**: Fácil adicionar novos temas
7. **Compatibilidade**: Melhor suporte a futuras versões do Streamlit

### 📚 Referências

- [Streamlit Theming Documentation](https://docs.streamlit.io/develop/concepts/configuration/theming)
- [Spotify Design System Colors](https://developer.spotify.com/documentation/general/design-and-branding/)

### 🔄 Migração

Se você estava usando a versão 1.x com Bootstrap:

1. **Backup**: Faça backup da versão anterior se necessário
2. **Atualize os arquivos**: `app.py`, `diagram_renderer.py`
3. **Adicione**: `.streamlit/config.toml`
4. **Remova**: Não há arquivos para remover, apenas substitua
5. **Teste**: Execute `streamlit run app.py`

### ⚠️ Breaking Changes

- Remoção completa de Bootstrap e Font Awesome
- Mudança na estrutura de navegação (botões → radio)
- Remoção de tooltips customizados (agora usa nativo do Streamlit)
- Remoção da feature "Enter to Apply"
- Cores personalizadas migradas para config.toml

---

## [1.0.0] - 2025-11-XX

### Versão inicial
- Aplicação com Bootstrap e Font Awesome
- Tema dark customizado com CSS variables
- Sistema de navegação com botões e ícones
- Suporte a tooltips customizados
- Feature "Enter to Apply"
- ~2000 linhas de código
