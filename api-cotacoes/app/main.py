import os
from dataclasses import asdict

from fastapi import FastAPI, HTTPException

from app.cotacoes import ADAPTADORES, escolher_estrategia

app = FastAPI(title="API de Cotações")


@app.get("/health")
def health():
    # AMBIENTE é definido no deploy (staging ou production)
    return {"status": "ok", "ambiente": os.getenv("AMBIENTE", "local")}


@app.get("/cotacoes/{bolsa}/{ticker}")
def obter_cotacao(bolsa: str, ticker: str):
    adaptador = ADAPTADORES.get(bolsa.lower())
    if adaptador is None:
        raise HTTPException(status_code=404, detail="Bolsa não suportada")

    cotacao = adaptador.obter(ticker.upper())
    if cotacao is None:
        raise HTTPException(status_code=404, detail="Ticker não encontrado")

    analise = escolher_estrategia(cotacao).analisar(cotacao)
    return {**asdict(cotacao), "analise": analise}
