"""
Configurações da aplicação
"""

# Configurações de visualização
DIAGRAM_CONFIG = {
    'default_zoom': 1.0,
    'min_zoom': 0.5,
    'max_zoom': 2.0,
    'zoom_step': 0.1,
    'default_center_x': 400,
    'default_center_y': 300,
    'diagram_height': 600,
}

# Configurações de tabelas
TABLE_CONFIG = {
    'max_fields_in_diagram': 5,
    'default_table_spacing_x': 150,
    'default_table_spacing_y': 150,
    'default_position_x': 100,
    'default_position_y': 100,
}

# Tipos de dados suportados
SUPPORTED_DATA_TYPES = [
    "STRING",
    "INT",
    "BIGINT",
    "FLOAT",
    "DOUBLE",
    "DECIMAL",
    "BOOLEAN",
    "DATE",
    "TIMESTAMP",
    "ARRAY",
    "MAP",
    "STRUCT",
    "BINARY",
]

# Configurações SQL
SQL_CONFIG = {
    'default_catalog': 'main',
    'default_schema': 'default',
    'use_delta': True,
    'include_comments': True,
}

# Cores dos relacionamentos
RELATIONSHIP_COLORS = {
    '1:1': '#1976d2',   # Azul
    '1:N': '#7b1fa2',   # Roxo
    'N:1': '#f57c00',   # Laranja
    'N:N': '#c62828',   # Vermelho
}

# Tags comuns para sugestão
COMMON_TAGS = [
    'pii',
    'key',
    'foreign_key',
    'business',
    'financial',
    'audit',
    'contact',
    'classification',
    'inventory',
    'metrics',
    'dimension',
    'fact',
]

# Limites
LIMITS = {
    'max_tables': 50,
    'max_fields_per_table': 100,
    'max_relationships': 100,
    'max_table_name_length': 64,
    'max_field_name_length': 64,
}

# Validações
VALIDATION_RULES = {
    'table_name_pattern': r'^[a-zA-Z][a-zA-Z0-9_]*$',
    'field_name_pattern': r'^[a-zA-Z][a-zA-Z0-9_]*$',
    'allow_spaces_in_names': False,
}

