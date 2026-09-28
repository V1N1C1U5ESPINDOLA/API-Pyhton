"""Lógica de cotações: fontes simuladas, adaptadores e estratégias de análise."""

from dataclasses import dataclass
from typing import ClassVar


# ---------- Fontes de dados (simuladas, com formatos diferentes) ----------
class FonteNasdaq:
    DADOS: ClassVar[dict[str, dict]] = {
        "AAPL": {"symbol": "AAPL", "price_usd": 190.50, "change_pct": 1.8},
        "MSFT": {"symbol": "MSFT", "price_usd": 410.10, "change_pct": -0.6},
    }

    def buscar(self, ticker: str) -> dict | None:
        return self.DADOS.get(ticker)


class FonteBovespa:
    DADOS: ClassVar[dict[str, dict]] = {
        "PETR4": {"codigo": "PETR4", "preco": 38.20, "variacao": -1.2},
        "VALE3": {"codigo": "VALE3", "preco": 61.75, "variacao": 0.4},
    }

    def consultar(self, codigo: str) -> dict | None:
        return self.DADOS.get(codigo)


# ---------- Formato único usado pela aplicação ----------
@dataclass
class Cotacao:
    ticker: str
    bolsa: str
    preco: float
    moeda: str
    variacao: float


# ---------- Adapter: converte cada fonte para o formato Cotacao ----------
class AdaptadorNasdaq:
    def __init__(self, fonte: FonteNasdaq | None = None):
        self.fonte = fonte or FonteNasdaq()

    def obter(self, ticker: str) -> Cotacao | None:
        dado = self.fonte.buscar(ticker)
        if dado is None:
            return None
        return Cotacao(dado["symbol"], "NASDAQ", dado["price_usd"], "USD", dado["change_pct"])


class AdaptadorBovespa:
    def __init__(self, fonte: FonteBovespa | None = None):
        self.fonte = fonte or FonteBovespa()

    def obter(self, ticker: str) -> Cotacao | None:
        dado = self.fonte.consultar(ticker)
        if dado is None:
            return None
        return Cotacao(dado["codigo"], "BOVESPA", dado["preco"], "BRL", dado["variacao"])


ADAPTADORES = {"nasdaq": AdaptadorNasdaq(), "bovespa": AdaptadorBovespa()}


# ---------- Strategy: análise muda conforme o mercado sobe ou cai ----------
class EstrategiaAlta:
    def analisar(self, cotacao: Cotacao) -> str:
        return f"{cotacao.ticker} em alta de {cotacao.variacao}%: considere realizar lucro."


class EstrategiaBaixa:
    def analisar(self, cotacao: Cotacao) -> str:
        return f"{cotacao.ticker} em queda de {abs(cotacao.variacao)}%: possível oportunidade de compra."


class EstrategiaEstavel:
    def analisar(self, cotacao: Cotacao) -> str:
        return f"{cotacao.ticker} estável: nenhuma ação recomendada."


def escolher_estrategia(cotacao: Cotacao):
    if cotacao.variacao > 0.5:
        return EstrategiaAlta()
    if cotacao.variacao < -0.5:
        return EstrategiaBaixa()
    return EstrategiaEstavel()
