# 🚀 Guia de Deployment - Databricks Apps

## Pré-requisitos

- Conta Databricks (não suportado em Standard Tier)
- Databricks CLI instalado e configurado
- Workspace com Apps habilitado
- Permissões adequadas para criar apps

## Método 1: Deploy via Databricks CLI (Recomendado)

### Passo 1: Instalar Databricks CLI

```bash
# Via pip
pip install databricks-cli

# Ou via Homebrew (macOS)
brew tap databricks/tap
brew install databricks
```

### Passo 2: Configurar Autenticação

```bash
databricks configure --token
```

Você precisará fornecer:
- Host do Databricks (ex: `https://seu-workspace.databricks.com`)
- Token de acesso (gere em User Settings > Access Tokens)

### Passo 3: Deploy do App

```bash
# Na pasta do projeto
cd data-modeling

# Deploy
databricks apps deploy data-modeling
```

### Passo 4: Verificar Status

```bash
databricks apps list
databricks apps get data-modeling
```

### Passo 5: Acessar o App

O CLI retornará a URL do app. Exemplo:
```
https://seu-workspace.databricks.com/apps/data-modeling
```

## Método 2: Deploy via Interface Web

### Passo 1: Empacotar o App

Crie um arquivo ZIP com todos os arquivos:

```bash
zip -r data-modeling.zip . -x "*.git*" "*.pyc" "__pycache__/*" "*.log"
```

### Passo 2: Upload via UI

1. Acesse seu Databricks Workspace
2. No menu lateral, clique em **Apps**
3. Clique em **Create App**
4. Preencha as informações:
   - **Name**: `data-modeling`
   - **Description**: `Aplicação de modelagem de dados visual`
5. Faça upload do arquivo `data-modeling.zip`
6. Configure os recursos:
   - **Memory**: 2Gi (recomendado)
   - **CPU**: 1 core
7. Clique em **Deploy**

### Passo 3: Configurar Permissões

1. Vá para as configurações do app
2. Em **Permissions**, adicione usuários ou grupos
3. Defina níveis de acesso:
   - **Can View**: Pode visualizar o app
   - **Can Run**: Pode usar o app
   - **Can Manage**: Pode modificar configurações

## Método 3: Deploy via API REST

### Usando cURL

```bash
# Criar/Atualizar App
curl -X POST https://seu-workspace.databricks.com/api/2.0/apps \
  -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-modeling",
    "description": "Data Modeling Application",
    "source_code_path": "/Workspace/Users/seu-email@exemplo.com/data-modeling"
  }'
```

### Usando Python

```python
import requests

url = "https://seu-workspace.databricks.com/api/2.0/apps"
headers = {
    "Authorization": f"Bearer {databricks_token}",
    "Content-Type": "application/json"
}
data = {
    "name": "data-modeling",
    "description": "Data Modeling Application",
    "source_code_path": "/Workspace/Users/seu-email@exemplo.com/data-modeling"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## Configurações Avançadas

### Ajustar Recursos (app.yaml)

```yaml
command: ["streamlit", "run", "app.py", "--server.port", "8080"]

resources:
  - name: default
    memory: 4Gi      # Aumente para modelos grandes
    cpu: 2           # Aumente para melhor performance

env:
  - name: STREAMLIT_THEME_PRIMARY_COLOR
    value: "#FF3621"
  - name: STREAMLIT_SERVER_MAX_UPLOAD_SIZE
    value: "200"
```

### Variáveis de Ambiente

Adicione no `app.yaml`:

```yaml
env:
  - name: DEFAULT_CATALOG
    value: "main"
  - name: DEFAULT_SCHEMA
    value: "default"
  - name: MAX_TABLES
    value: "50"
```

## Configuração de Rede

### Acesso Privado (VPC)

Para workspaces com rede privada, configure no `app.yaml`:

```yaml
network:
  private_endpoint: true
  vpc_id: "vpc-xxxxx"
```

### Whitelist de IPs

No Databricks Workspace Settings:
1. Admin Console > Security
2. IP Access Lists
3. Adicione IPs permitidos

## Monitoramento e Logs

### Visualizar Logs

```bash
# Via CLI
databricks apps logs data-modeling

# Em tempo real
databricks apps logs data-modeling --follow
```

### Via UI

1. Apps > data-modeling
2. Aba **Logs**
3. Configure filtros e alertas

### Métricas

O app reporta automaticamente:
- Uso de CPU e memória
- Número de usuários ativos
- Erros e exceções
- Tempo de resposta

## Atualizações

### Update Incremental

```bash
# Modificar código
# ...

# Deploy novamente
databricks apps deploy data-modeling --update
```

### Rollback

```bash
# Listar versões
databricks apps versions data-modeling

# Rollback para versão anterior
databricks apps rollback data-modeling --version 1
```

## Troubleshooting

### App não inicia

**Verificar:**
- Arquivo `app.yaml` está correto
- Todas as dependências estão em `requirements.txt`
- Nenhum arquivo excede 10MB
- Logs do app para erros

```bash
databricks apps logs data-modeling | grep ERROR
```

### Erro de dependências

**Solução:**
- Fixe versões no `requirements.txt`
- Use versões compatíveis
- Teste localmente primeiro

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Performance lenta

**Otimizações:**
- Aumente recursos no `app.yaml`
- Use cache do Streamlit: `@st.cache_data`
- Reduza física do diagrama
- Otimize queries SQL

### Erro de permissão

**Verificar:**
- Token tem permissões adequadas
- Usuário tem acesso ao workspace
- Service Principal configurado (se aplicável)

## Backup e Restore

### Backup Automático

Os modelos salvos em JSON servem como backup:

```bash
# Exportar todos os modelos
# (via UI, em cada projeto)
```

### Backup do App

```bash
# Clonar código fonte
git clone <repo-url>

# Backup de configurações
databricks apps get data-modeling > app-config.json
```

## Custos

### Estimativa de Custos

- Compute: ~$0.15/hora (2Gi, 1 CPU)
- Storage: Negligível (< 1GB)
- Network: Incluído

**Otimizar custos:**
- Configure auto-suspend (padrão: 10 min de inatividade)
- Use compute mínimo necessário
- Monitore uso com dashboards

## Checklist de Deploy

- [ ] Código testado localmente
- [ ] `requirements.txt` atualizado
- [ ] `app.yaml` configurado corretamente
- [ ] Documentação atualizada
- [ ] Testes passando (`python3 test_app.py`)
- [ ] CLI configurado
- [ ] Permissões definidas
- [ ] Variáveis de ambiente configuradas
- [ ] Backup do código realizado
- [ ] Monitoramento configurado

## Suporte

### Documentação Oficial
- [Databricks Apps Docs](https://docs.databricks.com/dev-tools/databricks-apps)
- [Databricks Apps Cookbook](https://apps-cookbook.dev/)

### Logs e Debug
```bash
# Logs detalhados
databricks apps logs data-modeling --level debug

# Status do app
databricks apps status data-modeling
```

### Contato
- Suporte Databricks: support@databricks.com
- Community: community.databricks.com

---

**✅ App pronto para produção!**

