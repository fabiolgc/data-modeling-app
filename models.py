"""
Modelos de dados para a aplicação de modelagem
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import json


class RelationshipType(Enum):
    """Tipos de relacionamento entre tabelas"""
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_ONE = "N:1"
    MANY_TO_MANY = "N:N"


@dataclass
class Field:
    """Campo de uma tabela"""
    name: str
    data_type: str
    description: Optional[str] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_nullable: bool = True
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'name': self.name,
            'data_type': self.data_type,
            'description': self.description,
            'is_primary_key': self.is_primary_key,
            'is_foreign_key': self.is_foreign_key,
            'is_nullable': self.is_nullable,
            'tags': self.tags
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Field':
        """Cria a partir de dicionário"""
        return Field(
            name=data['name'],
            data_type=data['data_type'],
            description=data.get('description'),
            is_primary_key=data.get('is_primary_key', False),
            is_foreign_key=data.get('is_foreign_key', False),
            is_nullable=data.get('is_nullable', True),
            tags=data.get('tags', [])
        )


@dataclass
class Table:
    """Tabela do modelo de dados"""
    name: str
    description: Optional[str] = None
    fields: List[Field] = field(default_factory=list)
    position_x: float = 0
    position_y: float = 0
    
    def add_field(self, field_obj: Field):
        """Adiciona um campo à tabela"""
        # Verifica se já existe um campo com esse nome
        if not any(f.name == field_obj.name for f in self.fields):
            self.fields.append(field_obj)
    
    def remove_field(self, field_name: str):
        """Remove um campo da tabela"""
        self.fields = [f for f in self.fields if f.name != field_name]
    
    def get_primary_keys(self) -> List[Field]:
        """Retorna os campos que são chave primária"""
        return [f for f in self.fields if f.is_primary_key]
    
    def get_foreign_keys(self) -> List[Field]:
        """Retorna os campos que são chave estrangeira"""
        return [f for f in self.fields if f.is_foreign_key]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'name': self.name,
            'description': self.description,
            'fields': [f.to_dict() for f in self.fields],
            'position_x': self.position_x,
            'position_y': self.position_y
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Table':
        """Cria a partir de dicionário"""
        return Table(
            name=data['name'],
            description=data.get('description'),
            fields=[Field.from_dict(f) for f in data.get('fields', [])],
            position_x=data.get('position_x', 0),
            position_y=data.get('position_y', 0)
        )


@dataclass
class Relationship:
    """Relacionamento entre tabelas"""
    from_table: str
    to_table: str
    relationship_type: RelationshipType
    from_field: Optional[str] = None
    to_field: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'from_table': self.from_table,
            'to_table': self.to_table,
            'relationship_type': self.relationship_type.value,
            'from_field': self.from_field,
            'to_field': self.to_field
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Relationship':
        """Cria a partir de dicionário"""
        return Relationship(
            from_table=data['from_table'],
            to_table=data['to_table'],
            relationship_type=RelationshipType(data['relationship_type']),
            from_field=data.get('from_field'),
            to_field=data.get('to_field')
        )


class DataModel:
    """Modelo de dados completo"""
    
    def __init__(self):
        self.tables: Dict[str, Table] = {}
        self.relationships: List[Relationship] = []
        self.metadata: Dict = {
            'name': 'Untitled Model',
            'version': '1.0',
            'description': ''
        }
    
    def add_table(self, table: Table):
        """Adiciona uma tabela ao modelo"""
        self.tables[table.name] = table
    
    def remove_table(self, table_name: str):
        """Remove uma tabela do modelo"""
        if table_name in self.tables:
            del self.tables[table_name]
            # Remove relacionamentos associados
            self.relationships = [
                r for r in self.relationships 
                if r.from_table != table_name and r.to_table != table_name
            ]
    
    def rename_table(self, old_name: str, new_name: str):
        """Renomeia uma tabela"""
        if old_name in self.tables:
            table = self.tables[old_name]
            table.name = new_name
            self.tables[new_name] = table
            del self.tables[old_name]
            
            # Atualiza relacionamentos
            for rel in self.relationships:
                if rel.from_table == old_name:
                    rel.from_table = new_name
                if rel.to_table == old_name:
                    rel.to_table = new_name
    
    def add_relationship(self, relationship: Relationship):
        """Adiciona um relacionamento ao modelo"""
        # Verifica se as tabelas existem
        if (relationship.from_table in self.tables and 
            relationship.to_table in self.tables):
            # Evita duplicatas
            if not any(
                r.from_table == relationship.from_table and 
                r.to_table == relationship.to_table 
                for r in self.relationships
            ):
                self.relationships.append(relationship)
    
    def remove_relationship(self, from_table: str, to_table: str):
        """Remove um relacionamento"""
        self.relationships = [
            r for r in self.relationships 
            if not (r.from_table == from_table and r.to_table == to_table)
        ]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'metadata': self.metadata,
            'tables': {name: table.to_dict() for name, table in self.tables.items()},
            'relationships': [r.to_dict() for r in self.relationships]
        }
    
    def to_json(self) -> str:
        """Converte para JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @staticmethod
    def from_dict(data: Dict) -> 'DataModel':
        """Cria a partir de dicionário"""
        model = DataModel()
        model.metadata = data.get('metadata', model.metadata)
        
        # Carrega tabelas
        for table_data in data.get('tables', {}).values():
            table = Table.from_dict(table_data)
            model.add_table(table)
        
        # Carrega relacionamentos
        for rel_data in data.get('relationships', []):
            rel = Relationship.from_dict(rel_data)
            model.add_relationship(rel)
        
        return model
    
    @staticmethod
    def from_json(json_str: str) -> 'DataModel':
        """Cria a partir de JSON"""
        data = json.loads(json_str)
        return DataModel.from_dict(data)

