# 🚀 Guia de Início Rápido

## 5 Minutos para seu Primeiro Modelo

### 1️⃣ Instalar e Executar (Local)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o app
streamlit run app.py
```

O app abrirá no navegador em `http://localhost:8501`

### 2️⃣ Criar sua Primeira Tabela

1. No painel lateral esquerdo, clique na aba **➕ Criar**
2. Digite o nome da tabela: `customers`
3. Adicione uma descrição: `Tabela de clientes`
4. Clique em **➕ Adicionar Tabela**

✅ Sua primeira tabela aparecerá no diagrama central!

### 3️⃣ Adicionar Campos

1. Clique na tabela `customers` no diagrama
2. No painel direito, expanda **📝 Campos**
3. Adicione os seguintes campos:

**Campo 1:**
- Nome: `customer_id`
- Tipo: `BIGINT`
- Descrição: `ID único do cliente`
- ✓ Chave Primária
- Tags: `pii, key`
- Clique **➕ Adicionar Campo**

**Campo 2:**
- Nome: `email`
- Tipo: `STRING`
- Descrição: `Email do cliente`
- Tags: `pii, contact`
- Clique **➕ Adicionar Campo**

**Campo 3:**
- Nome: `name`
- Tipo: `STRING`
- Descrição: `Nome completo`
- Tags: `pii`
- Clique **➕ Adicionar Campo**

### 4️⃣ Criar Segunda Tabela

Repita o processo para criar uma tabela `orders`:

1. Nome: `orders`
2. Descrição: `Pedidos dos clientes`
3. Campos:
   - `order_id` (BIGINT, PK)
   - `customer_id` (BIGINT, FK)
   - `order_date` (TIMESTAMP)
   - `total` (DECIMAL)

### 5️⃣ Criar Relacionamento

1. No painel lateral, aba **➕ Criar**
2. Role até **Novo Relacionamento**
3. Configure:
   - **De:** `orders`
   - **Para:** `customers`
   - **Tipo:** `N:1` (Muitos para Um)
4. Clique em **🔗 Adicionar Relacionamento**

🎉 Você verá uma linha conectando as duas tabelas!

### 6️⃣ Gerar SQL

1. Vá para a aba **💾 Salvar/Carregar**
2. Clique em **📝 Gerar DDL**
3. O código SQL aparecerá no painel central
4. Clique em **⬇️ Download DDL** para baixar

### 7️⃣ Salvar seu Trabalho

1. Aba **💾 Salvar/Carregar**
2. Clique em **📥 Exportar JSON**
3. Clique em **⬇️ Download JSON**
4. Salve o arquivo para uso futuro

## 🎯 Exemplo Completo Pronto

Quer começar com um exemplo? Importe o modelo de e-commerce:

1. Aba **💾 Salvar/Carregar**
2. Faça upload do arquivo `examples/ecommerce_model.json`
3. Clique em **📤 Importar**

Você terá um modelo completo com 4 tabelas e relacionamentos! 🎨

## ⚡ Dicas Rápidas

- **Zoom:** Use o slider na aba **🔧 Configurações**
- **Reorganizar:** Arraste as tabelas no diagrama
- **Editar:** Clique na tabela e modifique no painel direito
- **Excluir:** Selecione a tabela e clique em **🗑️ Excluir**

## 🚀 Deploy no Databricks

### Método Rápido (CLI)

```bash
# Configure o Databricks CLI (apenas uma vez)
databricks configure

# Deploy
databricks apps deploy data-modeling
```

### Método UI

1. Acesse seu Databricks Workspace
2. Vá para **Databricks Apps**
3. Clique **Create App**
4. Faça upload dos arquivos
5. Deploy! 🎉

## 📚 Próximos Passos

- Explore os [casos de uso avançados](README.md#-casos-de-uso-avançados)
- Personalize [configurações](config.py)
- Contribua com o projeto!

## ❓ Precisa de Ajuda?

Consulte o [README completo](README.md) para documentação detalhada.

---

**Pronto!** Você criou seu primeiro modelo de dados em menos de 5 minutos! 🎊

