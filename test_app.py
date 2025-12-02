"""
Testes para verificar a aplicação
"""

import json
from models import DataModel, Table, Field, Relationship, RelationshipType
from sql_generator import generate_ddl


def test_create_table():
    """Testa criação de tabela"""
    table = Table(name="test_table", description="Test description")
    field = Field(name="id", data_type="BIGINT", is_primary_key=True)
    table.add_field(field)
    
    assert len(table.fields) == 1
    assert table.fields[0].name == "id"
    print("✅ test_create_table passou!")


def test_data_model():
    """Testa modelo de dados completo"""
    model = DataModel()
    
    # Criar tabelas
    customers = Table(name="customers", description="Customers table")
    customers.add_field(Field(name="id", data_type="BIGINT", is_primary_key=True))
    customers.add_field(Field(name="name", data_type="STRING"))
    
    orders = Table(name="orders", description="Orders table")
    orders.add_field(Field(name="id", data_type="BIGINT", is_primary_key=True))
    orders.add_field(Field(name="customer_id", data_type="BIGINT", is_foreign_key=True))
    
    # Adicionar ao modelo
    model.add_table(customers)
    model.add_table(orders)
    
    # Criar relacionamento
    rel = Relationship(
        from_table="orders",
        to_table="customers",
        relationship_type=RelationshipType.MANY_TO_ONE
    )
    model.add_relationship(rel)
    
    assert len(model.tables) == 2
    assert len(model.relationships) == 1
    print("✅ test_data_model passou!")


def test_json_export_import():
    """Testa export e import JSON"""
    model = DataModel()
    
    table = Table(name="test", description="Test table")
    table.add_field(Field(name="id", data_type="BIGINT", is_primary_key=True))
    model.add_table(table)
    
    # Export
    json_str = model.to_json()
    assert json_str is not None
    
    # Import
    model2 = DataModel.from_json(json_str)
    assert len(model2.tables) == 1
    assert "test" in model2.tables
    print("✅ test_json_export_import passou!")


def test_sql_generation():
    """Testa geração de SQL DDL"""
    model = DataModel()
    
    table = Table(name="users", description="Users table")
    table.add_field(Field(
        name="user_id",
        data_type="BIGINT",
        description="User ID",
        is_primary_key=True,
        is_nullable=False
    ))
    table.add_field(Field(
        name="email",
        data_type="STRING",
        description="User email",
        is_nullable=False
    ))
    
    model.add_table(table)
    
    # Gerar DDL
    ddl = generate_ddl(model)
    
    assert "CREATE TABLE" in ddl
    assert "users" in ddl
    assert "user_id" in ddl
    assert "email" in ddl
    assert "PRIMARY KEY" in ddl
    print("✅ test_sql_generation passou!")


def test_relationship_types():
    """Testa tipos de relacionamento"""
    rel1 = Relationship("t1", "t2", RelationshipType.ONE_TO_ONE)
    rel2 = Relationship("t1", "t2", RelationshipType.ONE_TO_MANY)
    rel3 = Relationship("t1", "t2", RelationshipType.MANY_TO_ONE)
    rel4 = Relationship("t1", "t2", RelationshipType.MANY_TO_MANY)
    
    assert rel1.relationship_type == RelationshipType.ONE_TO_ONE
    assert rel2.relationship_type == RelationshipType.ONE_TO_MANY
    assert rel3.relationship_type == RelationshipType.MANY_TO_ONE
    assert rel4.relationship_type == RelationshipType.MANY_TO_MANY
    print("✅ test_relationship_types passou!")


def run_all_tests():
    """Executa todos os testes"""
    print("\n🧪 Executando testes...\n")
    
    try:
        test_create_table()
        test_data_model()
        test_json_export_import()
        test_sql_generation()
        test_relationship_types()
        
        print("\n✅ Todos os testes passaram! ✅\n")
        return True
    except AssertionError as e:
        print(f"\n❌ Teste falhou: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

