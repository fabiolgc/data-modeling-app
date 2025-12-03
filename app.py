"""
Data Modeling App - Databricks Apps
Aplicação para modelagem de dados visual no-code
Usando Streamlit Native Theming (Spotify Dark Theme)
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from models import DataModel, Table, Field, Relationship, RelationshipType
from sql_generator import generate_ddl
from diagram_renderer import render_diagram

# Configuração da página
st.set_page_config(
    page_title="Data Modeling - Databricks",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS mínimo apenas para ajustes finos
st.markdown("""
<style>
    /* Remove elementos desnecessários do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajuste do iframe para fundo transparente */
    iframe {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Compactar espaçamentos */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* Remover elementos vazios que aparecem antes do diagrama */
    .main [data-testid="column"] > div:empty {
        display: none !important;
    }
    
    .main .element-container:empty {
        display: none !important;
    }
    
    /* Remover espaçamentos extras antes do diagrama */
    .diagram-panel::before {
        display: none !important;
    }
    
    /* Melhorar legibilidade de badges */
    .stMarkdown code {
        background-color: rgba(29, 185, 84, 0.1);
        color: #1DB954;
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-size: 0.875rem;
    }
    
    /* Borda fina no painel do diagrama */
    .diagram-panel {
        border: 1px solid rgba(29, 185, 84, 0.3) !important;
        border-radius: 8px !important;
        padding: 0 !important;
        background-color: transparent !important;
        overflow: hidden !important;
    }
    
    /* Remover qualquer espaçamento extra no container do diagrama */
    .diagram-panel > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Ajustar iframe para não cortar bordas */
    .diagram-panel iframe {
        border-radius: 8px !important;
        display: block !important;
        margin: 0 !important;
    }
    
    /* Ocultar controles de zoom/reset do Mermaid */
    .mermaid-controls,
    .mermaid svg .reset,
    .mermaid .zoom-controls,
    svg .zoom-button,
    svg .reset-button,
    svg g[class*="zoom"],
    svg g[class*="reset"],
    svg g > g > g:first-child,
    svg > g > g:first-child {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    /* Ocultar elementos de controle dentro do iframe do Mermaid */
    iframe {
        pointer-events: auto !important;
    }
    
    /* Forçar ocultar grupo de controles no SVG */
    svg > g > g:first-of-type > rect[fill="#f2f2f2"],
    svg > g > g:first-of-type > text {
        display: none !important;
    }
    
    /* Esconder qualquer rect ou text que pareça ser um botão */
    svg g[transform] > rect[rx="5"],
    svg g[transform] > text[text-anchor="middle"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'data_model' not in st.session_state:
    st.session_state.data_model = DataModel()

if 'selected_table' not in st.session_state:
    st.session_state.selected_table = None

if 'diagram_config' not in st.session_state:
    st.session_state.diagram_config = {
        'zoom': 1.0,
        'center_x': 400,
        'center_y': 300
    }

if 'expanded_field' not in st.session_state:
    st.session_state.expanded_field = None

if 'table_form_key' not in st.session_state:
    st.session_state.table_form_key = 0

if 'field_form_key' not in st.session_state:
    st.session_state.field_form_key = 0

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "create"

# Sidebar - Ferramentas
with st.sidebar:
    st.title("🗄️ Data Modeling")
    st.caption("Modelagem visual de dados no-code")
    st.divider()
    
    # Navegação com tabs
    tab = st.radio(
        "Ferramentas",
        ["➕ Criar", "💾 Salvar/Carregar", "⚙️ Configurações"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # TAB: CRIAR
    if tab == "➕ Criar":
        st.subheader("Nova Tabela")
        
        new_table_name = st.text_input(
            "Nome da Tabela", 
            key=f"new_table_name_{st.session_state.table_form_key}"
        )
        new_table_desc = st.text_area(
            "Descrição", 
            key=f"new_table_desc_{st.session_state.table_form_key}", 
            height=80
        )
        
        if st.button("➕ Adicionar Tabela", type="primary", use_container_width=True):
            if new_table_name:
                if new_table_name not in st.session_state.data_model.tables:
                    table = Table(
                        name=new_table_name,
                        description=new_table_desc,
                        position_x=100 + len(st.session_state.data_model.tables) * 150,
                        position_y=100 + (len(st.session_state.data_model.tables) % 3) * 150
                    )
                    st.session_state.data_model.add_table(table)
                    st.session_state.selected_table = new_table_name
                    st.session_state.table_form_key += 1
                    st.success(f"✅ Tabela '{new_table_name}' criada!")
                    st.rerun()
                else:
                    st.error("❌ Já existe uma tabela com este nome.")
            else:
                st.warning("⚠️ Digite um nome para a tabela.")
        
        st.divider()
        
        st.subheader("Novo Relacionamento")
        if len(st.session_state.data_model.tables) >= 2:
            table_names = list(st.session_state.data_model.tables.keys())
            from_table = st.selectbox("De", table_names, key="rel_from")
            to_table = st.selectbox("Para", table_names, key="rel_to")
            rel_type = st.selectbox(
                "Tipo",
                [e.value for e in RelationshipType],
                key="rel_type"
            )
            
            # Campos das tabelas selecionadas
            col1, col2 = st.columns(2)
            with col1:
                from_fields = [""] + [f.name for f in st.session_state.data_model.tables[from_table].fields]
                from_field = st.selectbox(
                    f"Campo de {from_table}",
                    from_fields,
                    key="rel_from_field",
                    help="Campo que se relaciona"
                )
            with col2:
                to_fields = [""] + [f.name for f in st.session_state.data_model.tables[to_table].fields]
                to_field = st.selectbox(
                    f"Campo de {to_table}",
                    to_fields,
                    key="rel_to_field",
                    help="Campo relacionado"
                )
            
            if st.button("🔗 Adicionar Relacionamento", type="primary", use_container_width=True):
                if from_table != to_table:
                    rel = Relationship(
                        from_table=from_table,
                        to_table=to_table,
                        relationship_type=RelationshipType(rel_type),
                        from_field=from_field if from_field else None,
                        to_field=to_field if to_field else None
                    )
                    st.session_state.data_model.add_relationship(rel)
                    st.success("✅ Relacionamento criado!")
                    st.rerun()
                else:
                    st.warning("⚠️ Selecione tabelas diferentes")
        else:
            st.info("ℹ️ Crie pelo menos 2 tabelas para adicionar relacionamentos")
    
    # TAB: SALVAR/CARREGAR
    elif tab == "💾 Salvar/Carregar":
        st.subheader("Exportar Modelo")
        if st.button("📥 Exportar JSON", use_container_width=True):
            json_data = st.session_state.data_model.to_json()
            st.download_button(
                label="⬇️ Download JSON",
                data=json_data,
                file_name=f"data_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.divider()
        
        st.subheader("Importar Modelo")
        uploaded_file = st.file_uploader("Carregar JSON", type=['json'])
        if uploaded_file:
            if st.button("📤 Importar", type="primary", use_container_width=True):
                try:
                    json_content = uploaded_file.read().decode('utf-8')
                    st.session_state.data_model = DataModel.from_json(json_content)
                    st.session_state.selected_table = None
                    st.success("✅ Modelo importado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
        
        st.divider()
        
        st.subheader("Gerar SQL DDL")
        if st.button("📝 Gerar DDL", type="primary", use_container_width=True):
            if st.session_state.data_model.tables:
                ddl = generate_ddl(st.session_state.data_model)
                st.session_state.generated_ddl = ddl
                st.success("✅ DDL gerado!")
            else:
                st.warning("⚠️ Crie tabelas primeiro")
    
    # TAB: CONFIGURAÇÕES
    elif tab == "⚙️ Configurações":
        st.subheader("Configurações")
        
        st.info("ℹ️ O diagrama Mermaid ERD é renderizado automaticamente com layout otimizado.")
        
        st.divider()
        
        st.subheader("Gerenciar Modelo")
        if st.button("🗑️ Limpar Modelo", type="secondary", use_container_width=True):
            if st.checkbox("⚠️ Confirmar limpeza?"):
                st.session_state.data_model = DataModel()
                st.session_state.selected_table = None
                st.success("✅ Modelo limpo!")
                st.rerun()

# Layout principal
main_col, detail_col = st.columns([2.5, 1], gap="large")

# Coluna principal - Diagrama
with main_col:
    if st.session_state.data_model.tables:
        # Container com borda para o diagrama (sem título acima)
        st.markdown('<div class="diagram-panel">', unsafe_allow_html=True)
        
        render_diagram(
            st.session_state.data_model,
            st.session_state.diagram_config,
            st.session_state.selected_table
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Seletor de tabela manual abaixo do diagrama
        if len(st.session_state.data_model.tables) > 0:
            st.markdown("---")
            st.caption("📋 Selecione uma tabela para ver/editar detalhes:")
            table_names = ["(Nenhuma selecionada)"] + list(st.session_state.data_model.tables.keys())
            selected = st.selectbox(
                "Selecionar tabela",
                table_names,
                index=0 if not st.session_state.selected_table else table_names.index(st.session_state.selected_table) if st.session_state.selected_table in table_names else 0,
                key="table_selector",
                label_visibility="collapsed"
            )
            if selected and selected != "(Nenhuma selecionada)" and selected != st.session_state.selected_table:
                st.session_state.selected_table = selected
                st.rerun()
            elif selected == "(Nenhuma selecionada)" and st.session_state.selected_table:
                st.session_state.selected_table = None
                st.rerun()
        
        # Mostrar DDL gerado
        if 'generated_ddl' in st.session_state and st.session_state.generated_ddl:
            with st.expander("📝 SQL DDL Gerado", expanded=False):
                st.code(st.session_state.generated_ddl, language='sql')
                st.download_button(
                    label="⬇️ Download DDL",
                    data=st.session_state.generated_ddl,
                    file_name=f"schema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql",
                    mime="text/plain",
                    use_container_width=True
                )
    else:
        st.info("👈 Crie sua primeira tabela usando o painel lateral")

# Coluna de detalhes
with detail_col:
    if st.session_state.data_model.tables:
        st.subheader("📋 Detalhes")
    
    if st.session_state.selected_table:
        table = st.session_state.data_model.tables[st.session_state.selected_table]
        
        st.markdown(f"### 🗂️ {table.name}")
        
        # Editar tabela
        with st.expander("✏️ Editar Tabela", expanded=True):
            new_name = st.text_input("Nome", value=table.name, key="edit_table_name")
            new_desc = st.text_area("Descrição", value=table.description or "", key="edit_table_desc")
            
            col_save, col_delete = st.columns(2)
            with col_save:
                if st.button("💾 Salvar", key="save_table", use_container_width=True):
                    if new_name and new_name != table.name:
                        if new_name not in st.session_state.data_model.tables:
                            st.session_state.data_model.rename_table(table.name, new_name)
                            st.session_state.selected_table = new_name
                    table.description = new_desc
                    st.success("✅ Salvo!")
                    st.rerun()
            
            with col_delete:
                if st.button("🗑️ Excluir", key="delete_table", use_container_width=True):
                    st.session_state.data_model.remove_table(table.name)
                    st.session_state.selected_table = None
                    st.success("✅ Tabela excluída!")
                    st.rerun()
        
        # Gerenciar campos
        with st.expander("📝 Campos", expanded=True):
            st.markdown("**Adicionar Campo**")
            
            if 'field_form_key' not in st.session_state:
                st.session_state.field_form_key = 0
            
            col1, col2 = st.columns(2)
            with col1:
                field_name = st.text_input("Nome do Campo", key=f"new_field_name_{st.session_state.field_form_key}")
            with col2:
                field_type = st.selectbox(
                    "Tipo",
                    ["STRING", "INT", "BIGINT", "FLOAT", "DOUBLE", "DECIMAL", 
                     "BOOLEAN", "DATE", "TIMESTAMP", "ARRAY", "MAP", "STRUCT"],
                    key=f"new_field_type_{st.session_state.field_form_key}"
                )
            
            field_desc = st.text_input("Descrição", key=f"new_field_desc_{st.session_state.field_form_key}")
            
            col_pk, col_fk = st.columns(2)
            with col_pk:
                is_pk = st.checkbox("🔑 PK", key=f"new_field_pk_{st.session_state.field_form_key}")
            with col_fk:
                is_fk = st.checkbox("🔗 FK", key=f"new_field_fk_{st.session_state.field_form_key}")
            
            field_tags = st.text_input("Tags (separadas por vírgula)", key=f"new_field_tags_{st.session_state.field_form_key}")
            
            if st.button("➕ Adicionar Campo", type="primary", use_container_width=True):
                if field_name:
                    tags_list = [t.strip() for t in field_tags.split(',')] if field_tags else []
                    field = Field(
                        name=field_name,
                        data_type=field_type,
                        description=field_desc,
                        is_primary_key=is_pk,
                        is_foreign_key=is_fk,
                        tags=tags_list
                    )
                    table.add_field(field)
                    st.success(f"✅ Campo '{field_name}' adicionado!")
                    st.session_state.field_form_key += 1
                    st.rerun()
                else:
                    st.warning("⚠️ Digite um nome para o campo")
            
            st.divider()
            
            # Listar campos existentes usando st.table
            if table.fields:
                st.markdown("**Campos Existentes**")
                
                # Criar DataFrame para exibir em tabela
                import pandas as pd
                
                table_data = []
                for field in table.fields:
                    # PK/FK
                    pk_fk = ""
                    if field.is_primary_key:
                        pk_fk = "🔑 PK"
                    elif field.is_foreign_key:
                        pk_fk = "🔗 FK"
                    
                    # Null
                    nullable = "" if field.is_nullable else "NOT NULL"
                    
                    table_data.append({
                        "PK/FK": pk_fk,
                        "Campo": field.name,
                        "Tipo": field.data_type,
                        "Null": nullable,
                        "Descrição": field.description or ""
                    })
                
                # Criar DataFrame
                df_fields = pd.DataFrame(table_data)
                
                # Exibir tabela sem índice
                st.table(df_fields)
                
                # Botões de ação para cada campo
                st.markdown("**Ações**")
                for idx, field in enumerate(table.fields):
                    field_id = f"{table.name}_{field.name}"
                    col_field, col_del = st.columns([4, 1])
                    with col_field:
                        st.caption(f"• {field.name}")
                    with col_del:
                        if st.button("🗑️", key=f"del_field_{field_id}", help="Remover campo"):
                            table.remove_field(field.name)
                            st.success("✅ Campo removido!")
                            st.rerun()
            else:
                st.info("Nenhum campo ainda")
    
    # Mostrar relacionamentos
    if st.session_state.data_model.relationships:
        with st.expander("🔗 Relacionamentos", expanded=False):
            for rel in st.session_state.data_model.relationships:
                col_rel, col_del = st.columns([4, 1])
                with col_rel:
                    rel_text = f"**{rel.from_table}** → **{rel.to_table}**  \n`{rel.relationship_type.value}`"
                    if rel.from_field and rel.to_field:
                        rel_text += f"  \n🔗 `{rel.from_field}:{rel.to_field}`"
                    st.markdown(rel_text)
                with col_del:
                    if st.button("🗑️", key=f"del_rel_{rel.from_table}_{rel.to_table}", help="Remover"):
                        st.session_state.data_model.remove_relationship(rel.from_table, rel.to_table)
                        st.success("✅ Relacionamento removido!")
                        st.rerun()

# Footer
if st.session_state.data_model.tables or st.session_state.data_model.relationships:
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📊 Tabelas: {len(st.session_state.data_model.tables)}")
    with col2:
        st.caption(f"🔗 Relacionamentos: {len(st.session_state.data_model.relationships)}")
