"""
Renderizador de diagramas usando Mermaid
"""

import streamlit as st
import streamlit.components.v1 as components
from models import DataModel, Table, RelationshipType, Relationship
from typing import Optional, Dict, List


def get_relationship_symbol(rel_type: RelationshipType) -> str:
    """Retorna o símbolo de relacionamento para Mermaid ERD"""
    symbols = {
        RelationshipType.ONE_TO_ONE: "|o--o|",       # 1:1
        RelationshipType.ONE_TO_MANY: "|o--o{",      # 1:N
        RelationshipType.MANY_TO_ONE: "}o--o|",      # N:1
        RelationshipType.MANY_TO_MANY: "}o--o{"      # N:N
    }
    return symbols.get(rel_type, "|o--o|")


def create_mermaid_erd(model: DataModel, config: Dict) -> str:
    """
    Cria um diagrama ERD (Entity Relationship Diagram) usando sintaxe Mermaid
    """
    lines = ["erDiagram"]
    lines.append("")  # Linha vazia
    
    # Definir entidades (tabelas) com seus campos
    for table_name, table in model.tables.items():
        # Nome da tabela
        lines.append(f"    {table_name} {{")
        
        # Campos da tabela
        for field in table.fields[:10]:  # Limitar a 10 campos
            # Tipo de campo
            field_type = field.data_type.lower()
            
            # Marcadores
            markers = []
            if field.is_primary_key:
                markers.append("PK")
            if field.is_foreign_key:
                markers.append("FK")
            
            # Nullable
            nullable = "" if field.is_nullable else "NOT NULL"
            
            # Construir linha do campo
            marker_str = ",".join(markers) if markers else ""
            if marker_str and nullable:
                constraint = f"{marker_str},{nullable}"
            elif marker_str:
                constraint = marker_str
            elif nullable:
                constraint = nullable
            else:
                constraint = ""
            
            # Formato: tipo nome_campo "constraint"
            if constraint:
                lines.append(f'        {field_type} {field.name} "{constraint}"')
            else:
                lines.append(f'        {field_type} {field.name}')
        
        # Indicador de mais campos
        if len(table.fields) > 10:
            lines.append(f'        string more_fields "... +{len(table.fields) - 10} campos"')
        
        lines.append("    }")
        lines.append("")
    
    # Definir relacionamentos
    for rel in model.relationships:
        symbol = get_relationship_symbol(rel.relationship_type)
        
        # Label do relacionamento
        if rel.from_field and rel.to_field:
            label = f"{rel.relationship_type.value}({rel.from_field}:{rel.to_field})"
        else:
            label = rel.relationship_type.value
        
        # Formato: TABELA1 SIMBOLO TABELA2 : "label"
        lines.append(f'    {rel.from_table} {symbol} {rel.to_table} : "{label}"')
    
    return "\n".join(lines)


def render_diagram(
    model: DataModel,
    config: Dict,
    selected_table: Optional[str] = None
) -> Optional[str]:
    """
    Renderiza o diagrama do modelo de dados usando Mermaid
    Retorna o nome da tabela selecionada, se houver (não implementado em Mermaid)
    """
    if not model.tables:
        return None
    
    # Gerar código Mermaid
    mermaid_code = create_mermaid_erd(model, config)
    
    # Renderizar usando HTML customizado (sem controles de zoom/reset)
    try:
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background-color: #121212;
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    min-height: 100vh;
                }}
                .mermaid {{
                    background-color: transparent;
                }}
                /* Ocultar controles de zoom/reset */
                svg > g > g:first-of-type {{
                    display: none !important;
                }}
            </style>
        </head>
        <body>
            <div class="mermaid">
{mermaid_code}
            </div>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'dark',
                    themeVariables: {{
                        primaryColor: '#1DB954',
                        primaryTextColor: '#fff',
                        primaryBorderColor: '#1DB954',
                        lineColor: '#1DB954',
                        secondaryColor: '#282828',
                        tertiaryColor: '#121212'
                    }},
                    er: {{
                        useMaxWidth: true
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        components.html(html_code, height=600, scrolling=True)
        
    except Exception as e:
        st.error(f"Erro ao renderizar diagrama: {str(e)}")
        st.code(mermaid_code, language="mermaid")
        st.info("💡 Dica: O código Mermaid acima pode ser copiado e usado em documentação.")
    
    # Mermaid ERD não suporta seleção interativa nativamente
    return None


def render_simple_diagram(model: DataModel, selected_table: Optional[str] = None):
    """
    Renderiza um diagrama simples em texto quando Mermaid falhar
    """
    st.markdown("### Visualização Simplificada")
    
    # Listar tabelas
    for table_name, table in model.tables.items():
        with st.expander(f"📊 {table_name}", expanded=(table_name == selected_table)):
            if table.fields:
                st.markdown("**Campos:**")
                for field in table.fields:
                    pk_badge = "🔑" if field.is_primary_key else ""
                    fk_badge = "🔗" if field.is_foreign_key else ""
                    st.markdown(f"- {pk_badge}{fk_badge} **{field.name}** `{field.data_type}`")
            else:
                st.info("Nenhum campo")
    
    # Listar relacionamentos
    if model.relationships:
        st.markdown("---")
        st.markdown("### 🔗 Relacionamentos")
        for rel in model.relationships:
            rel_text = f"**{rel.from_table}** → **{rel.to_table}** `{rel.relationship_type.value}`"
            if rel.from_field and rel.to_field:
                rel_text += f" ({rel.from_field}:{rel.to_field})"
            st.markdown(rel_text)
