# API de Cotações — Pipeline de CI/CD

API simples em FastAPI que consulta cotações da NASDAQ e da BOVESPA (dados simulados),
usando os padrões **Adapter** (unifica o formato das bolsas) e **Strategy** (análise
muda conforme o mercado sobe ou cai).

## Rodar localmente
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
```

## Testes
```bash
pip install pytest pytest-cov
pytest --cov=app
```

## Pipeline (GitHub Actions)
`lint` + `codeql` → `test` → `build` (imagem Docker no GHCR) → `deploy-staging` → `dast` (OWASP ZAP) → `deploy-production` (com aprovação manual)

- **Estática:** Ruff, Bandit, CodeQL
- **Dinâmica:** pytest com cobertura, OWASP ZAP
- **Ambientes:** `staging` e `production`
