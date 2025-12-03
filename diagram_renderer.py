"""
Renderizador de diagramas para visualização de modelos de dados
"""

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from models import DataModel, Table, RelationshipType
from typing import Optional, Dict, List


def get_relationship_color(rel_type: RelationshipType) -> str:
    """Retorna a cor baseada no tipo de relacionamento - Spotify Theme"""
    colors = {
        RelationshipType.ONE_TO_ONE: "#1DB954",      # Spotify Green
        RelationshipType.ONE_TO_MANY: "#1ED760",     # Lighter Green
        RelationshipType.MANY_TO_ONE: "#535353",     # Gray
        RelationshipType.MANY_TO_MANY: "#B3B3B3"     # Light Gray
    }
    return colors.get(rel_type, "#1DB954")


def get_relationship_label(rel_type: RelationshipType) -> str:
    """Retorna o label do relacionamento"""
    return rel_type.value


def create_table_label(table: Table) -> str:
    """
    Cria o label para uma tabela em formato simples e limpo
    Usa espaços fixos para garantir alinhamento perfeito
    """
    # Limita o número de campos mostrados no diagrama
    max_fields = 8
    fields_to_show = table.fields[:max_fields]
    
    # Larguras fixas das colunas (em caracteres)
    w_pk = 5       # PK/FK
    sp1 = 3        # Espaçamento 1
    w_campo = 20   # Campo
    sp2 = 3        # Espaçamento 2
    w_tipo = 12    # Tipo
    sp3 = 3        # Espaçamento 3
    w_null = 8     # Null
    
    total_width = w_pk + sp1 + w_campo + sp2 + w_tipo + sp3 + w_null
    
    lines = []
    
    # Nome da tabela com borda
    lines.append("=" * total_width)
    nome_centralizado = table.name.upper().center(total_width)
    lines.append(nome_centralizado)
    lines.append("=" * total_width)
    
    # Cabeçalho - cada coluna com largura fixa
    h_pk = "PK/FK".ljust(w_pk)
    h_campo = "Campo".ljust(w_campo)
    h_tipo = "Tipo".ljust(w_tipo)
    h_null = "Null".ljust(w_null)
    header = h_pk + (" " * sp1) + h_campo + (" " * sp2) + h_tipo + (" " * sp3) + h_null
    lines.append(header)
    lines.append("-" * total_width)
    
    # Linhas de dados
    for field in fields_to_show:
        # Coluna 1: PK/FK (5 chars, alinhado à direita)
        if field.is_primary_key:
            pk_fk = "PK"
        elif field.is_foreign_key:
            pk_fk = "FK"
        else:
            pk_fk = ""
        c_pk = (" " * (w_pk - len(pk_fk))) + pk_fk
        
        # Coluna 2: Campo (20 chars, alinhado à esquerda)
        if len(field.name) > w_campo:
            campo_text = field.name[:w_campo-2] + ".."
        else:
            campo_text = field.name
        c_campo = campo_text + (" " * (w_campo - len(campo_text)))
        
        # Coluna 3: Tipo (12 chars, alinhado à esquerda)
        if len(field.data_type) > w_tipo:
            tipo_text = field.data_type[:w_tipo-2] + ".."
        else:
            tipo_text = field.data_type
        c_tipo = tipo_text + (" " * (w_tipo - len(tipo_text)))
        
        # Coluna 4: Null (8 chars, alinhado à esquerda)
        if field.is_nullable:
            null_text = ""
        else:
            null_text = "NOT NULL"
        c_null = null_text + (" " * (w_null - len(null_text)))
        
        # Montar linha completa
        linha = c_pk + (" " * sp1) + c_campo + (" " * sp2) + c_tipo + (" " * sp3) + c_null
        lines.append(linha)
    
    # Indicador de mais campos
    if len(table.fields) > max_fields:
        lines.append("-" * total_width)
        more_text = f"... +{len(table.fields) - max_fields} mais campos"
        lines.append(more_text.center(total_width))
    
    # Placeholder se não houver campos
    if not fields_to_show:
        lines.append("(nenhum campo)".center(total_width))
    
    # Linha final
    lines.append("=" * total_width)
    
    return "\n".join(lines)


def render_diagram(
    model: DataModel,
    config: Dict,
    selected_table: Optional[str] = None
) -> Optional[str]:
    """
    Renderiza o diagrama do modelo de dados
    Retorna o nome da tabela selecionada, se houver
    """
    if not model.tables:
        return None
    
    # Criar nodes (tabelas) - Spotify Theme
    nodes = []
    for table_name, table in model.tables.items():
        # Cor baseada em seleção - Spotify Green quando selecionado
        color = "#1DB954" if table_name == selected_table else "#282828"
        border_color = "#1DB954" if table_name == selected_table else "#535353"
        
        node = Node(
            id=table_name,
            label=create_table_label(table),
            size=450,
            color={
                "background": color,
                "border": border_color,
                "highlight": {
                    "background": "#1DB954",
                    "border": "#1ED760"
                }
            },
            shape="box",
            font={
                "size": 11, 
                "color": "#FFFFFF", 
                "face": "Courier New, monospace",  # Fonte monoespaçada para bordas
                "multi": "md",  # Markdown ao invés de HTML
                "align": "left",
                "vadjust": 0
            },
            x=table.position_x * config['zoom'],
            y=table.position_y * config['zoom'],
            borderWidth=2,
            borderWidthSelected=3,
            widthConstraint={"minimum": 450, "maximum": 450},
            heightConstraint={"minimum": 120},
            margin={"top": 10, "bottom": 10, "left": 10, "right": 10}
        )
        nodes.append(node)
    
    # Criar edges (relacionamentos)
    edges = []
    for rel in model.relationships:
        edge = Edge(
            source=rel.from_table,
            target=rel.to_table,
            label=get_relationship_label(rel.relationship_type),
            color=get_relationship_color(rel.relationship_type),
            width=3,
            arrows="to",
            # Configurações para linha curva e label visível
            smooth={
                "enabled": True,
                "type": "curvedCW",  # Curved ClockWise - linha curva
                "roundness": 0.2     # Curvatura moderada
            },
            font={
                "size": 14,
                "color": "#FFFFFF",
                "background": "#121212",
                "strokeWidth": 2,
                "strokeColor": "#121212",
                "align": "horizontal",
                "bold": True
            }
        )
        edges.append(edge)
    
    # Configuração do grafo - Spotify Theme
    graph_config = Config(
        width="100%",
        height=600,
        directed=True,
        backgroundColor="#121212",  # Spotify Dark Background
        physics={
            "enabled": True,
            "stabilization": {
                "enabled": True,
                "iterations": 100
            },
            "barnesHut": {
                "gravitationalConstant": -8000,
                "centralGravity": 0.3,
                "springLength": 200,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 1
            }
        },
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#1DB954",  # Spotify Green
        collapsible=False,
        node={
            "labelProperty": "label",
            "renderLabel": True
        },
        link={
            "labelProperty": "label",
            "renderLabel": True
        },
        # Configurações de edges para linhas curvas - Spotify Theme
        edges={
            "smooth": {
                "enabled": True,
                "type": "curvedCW",
                "roundness": 0.2
            },
            "font": {
                "size": 14,
                "align": "horizontal",
                "background": "#121212",
                "strokeWidth": 2,
                "strokeColor": "#121212",
                "color": "#FFFFFF"
            }
        },
        interaction={
            "dragNodes": True,
            "dragView": True,
            "zoomView": True,
            "hover": True,
            "navigationButtons": True,
            "keyboard": True
        }
    )
    
    # Renderizar o grafo
    try:
        return_value = agraph(
            nodes=nodes,
            edges=edges,
            config=graph_config
        )
        
        # Se um node foi clicado, retornar seu ID
        if return_value:
            return return_value
        
    except Exception as e:
        st.error(f"Erro ao renderizar diagrama: {str(e)}")
        # Fallback para visualização simples
        render_simple_diagram(model, selected_table)
    
    return None


def render_simple_diagram(model: DataModel, selected_table: Optional[str] = None):
    """
    Renderiza um diagrama simples usando HTML/CSS quando agraph falhar
    """
    st.markdown("### Visualização Simplificada")
    
    # Criar layout com colunas para tabelas
    num_tables = len(model.tables)
    
    if num_tables == 0:
        return
    
    # Organizar em grid
    cols_per_row = 3
    tables_list = list(model.tables.items())
    
    for i in range(0, num_tables, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < num_tables:
                table_name, table = tables_list[idx]
                with col:
                    render_table_card(table, selected_table == table_name)
    
    # Mostrar relacionamentos
    if model.relationships:
        st.markdown("---")
        st.markdown("#### 🔗 Relacionamentos")
        
        rel_cols = st.columns(2)
        for idx, rel in enumerate(model.relationships):
            with rel_cols[idx % 2]:
                rel_class = f"rel-{rel.relationship_type.value.lower().replace(':', '-')}"
                st.markdown(f"""
                <div class="relationship-badge {rel_class}">
                    {rel.from_table} → {rel.to_table} ({rel.relationship_type.value})
                </div>
                """, unsafe_allow_html=True)


def render_table_card(table: Table, is_selected: bool = False):
    """Renderiza um card de tabela em formato tabular - Spotify Theme"""
    border_color = "#1DB954" if is_selected else "#535353"  # Spotify Green or Gray
    
    # Construir HTML da tabela de campos
    fields_html = ""
    for field in table.fields[:5]:  # Mostrar no máximo 5 campos
        icon = ""
        icon_color = ""
        if field.is_primary_key:
            icon = "🔑"
            icon_color = "var(--db-blue)"
        elif field.is_foreign_key:
            icon = "🔗"
            icon_color = "var(--db-green)"
        
        nullable_badge = ""
        if not field.is_nullable:
            nullable_badge = '<span style="background: rgba(255,54,33,0.1); color: var(--db-coral); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 600;">NOT NULL</span>'
        
        fields_html += f"""
        <tr>
            <td style="padding: 6px 8px; border-bottom: 1px solid var(--db-light-gray); width: 30px;">
                <span style="color: {icon_color};">{icon}</span>
            </td>
            <td style="padding: 6px 8px; border-bottom: 1px solid var(--db-light-gray); font-weight: 600;">
                {field.name}
            </td>
            <td style="padding: 6px 8px; border-bottom: 1px solid var(--db-light-gray); color: var(--db-medium-gray); font-family: monospace; font-size: 0.85rem;">
                {field.data_type}
            </td>
            <td style="padding: 6px 8px; border-bottom: 1px solid var(--db-light-gray); text-align: right;">
                {nullable_badge}
            </td>
        </tr>
        """
    
    if len(table.fields) > 5:
        fields_html += f"""
        <tr>
            <td colspan="4" style="padding: 8px; text-align: center; color: var(--db-medium-gray); font-size: 0.85rem;">
                ... +{len(table.fields) - 5} campos
            </td>
        </tr>
        """
    
    if not table.fields:
        fields_html = """
        <tr>
            <td colspan="4" style="padding: 20px; text-align: center; color: var(--db-medium-gray);">
                Nenhum campo adicionado
            </td>
        </tr>
        """
    
    st.markdown(f"""
    <div style="
        background: var(--db-white);
        border: 2px solid {border_color};
        border-radius: 12px;
        overflow: hidden;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(27, 28, 30, 0.08);
        transition: all 0.2s ease;
    ">
        <div style="
            background: var(--db-white);
            padding: 1rem 1.25rem;
            border-bottom: 2px solid var(--db-light-gray);
        ">
            <h4 style="margin: 0; color: var(--db-black); font-weight: 700; font-size: 1.125rem;">
                {table.name}
            </h4>
            {f'<p style="color: var(--db-medium-gray); font-size: 0.875rem; margin: 0.5rem 0 0 0;">{table.description}</p>' if table.description else ''}
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            {fields_html}
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"Selecionar", key=f"btn_{table.name}", use_container_width=True, type="secondary"):
        st.session_state.selected_table = table.name
        st.rerun()


def render_mermaid_diagram(model: DataModel) -> str:
    """
    Gera código Mermaid para o diagrama ER
    Isso pode ser usado para export ou visualização alternativa
    """
    lines = ["erDiagram"]
    
    # Adicionar tabelas
    for table_name, table in model.tables.items():
        if table.fields:
            lines.append(f"    {table_name} {{")
            for field in table.fields:
                field_type = field.data_type.lower()
                key_marker = "PK" if field.is_primary_key else ("FK" if field.is_foreign_key else "")
                line = f"        {field_type} {field.name}"
                if key_marker:
                    line += f" {key_marker}"
                lines.append(line)
            lines.append("    }")
    
    # Adicionar relacionamentos
    for rel in model.relationships:
        # Converter tipos de relacionamento para formato Mermaid
        mermaid_rel = {
            RelationshipType.ONE_TO_ONE: "||--||",
            RelationshipType.ONE_TO_MANY: "||--o{",
            RelationshipType.MANY_TO_ONE: "}o--||",
            RelationshipType.MANY_TO_MANY: "}o--o{"
        }.get(rel.relationship_type, "||--||")
        
        lines.append(f"    {rel.from_table} {mermaid_rel} {rel.to_table} : has")
    
    return "\n".join(lines)


def export_diagram_as_svg(model: DataModel) -> str:
    """
    Exporta o diagrama como SVG (implementação futura)
    """
    # TODO: Implementar export SVG usando mermaid ou outra biblioteca
    return ""

