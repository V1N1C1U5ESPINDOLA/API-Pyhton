from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_cotacao_bovespa():
    r = client.get("/cotacoes/bovespa/petr4")
    assert r.status_code == 200
    assert r.json()["ticker"] == "PETR4"
    assert "queda" in r.json()["analise"]


def test_bolsa_invalida():
    assert client.get("/cotacoes/nyse/AAPL").status_code == 404


def test_ticker_invalido():
    assert client.get("/cotacoes/nasdaq/XYZ").status_code == 404
