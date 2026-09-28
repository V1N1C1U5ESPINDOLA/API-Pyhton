from app.cotacoes import (
    AdaptadorBovespa,
    AdaptadorNasdaq,
    Cotacao,
    EstrategiaAlta,
    EstrategiaBaixa,
    EstrategiaEstavel,
    escolher_estrategia,
)


def test_adaptador_nasdaq_converte_formato():
    c = AdaptadorNasdaq().obter("AAPL")
    assert c.bolsa == "NASDAQ" and c.moeda == "USD" and c.preco == 190.50


def test_adaptador_bovespa_converte_formato():
    c = AdaptadorBovespa().obter("PETR4")
    assert c.bolsa == "BOVESPA" and c.moeda == "BRL" and c.preco == 38.20


def test_ticker_inexistente_retorna_none():
    assert AdaptadorNasdaq().obter("XYZ") is None


def test_estrategia_varia_com_mercado():
    base = {"ticker": "T", "bolsa": "B", "preco": 1.0, "moeda": "BRL"}
    assert isinstance(escolher_estrategia(Cotacao(**base, variacao=2.0)), EstrategiaAlta)
    assert isinstance(escolher_estrategia(Cotacao(**base, variacao=-2.0)), EstrategiaBaixa)
    assert isinstance(escolher_estrategia(Cotacao(**base, variacao=0.1)), EstrategiaEstavel)
