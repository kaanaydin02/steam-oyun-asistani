"""FastAPI servisi: agent'ı HTTP üzerinden sunar. Çalıştırma: uvicorn src.api:app --port 8000"""
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src import llm, rag_araci
from src.agent_graf import calistir

# 09'un sonucu: varsayılan Luna, diğerleri seçilebilir (puana göre sıralı)
API_MODELLERI = ["gpt-6-luna", "deepseek-flash", "gpt-4.1-mini", "qwen2.5:7b"]
VARSAYILAN_MODEL = "gpt-6-luna"


@asynccontextmanager
async def yasam_dongusu(app):
    t = time.perf_counter()
    rag_araci.isinma()                      # embedding modeli + Chroma ilk sorguda yavaş; açılışta ısıt
    print(f"Isınma bitti: {time.perf_counter() - t:.1f} sn")
    yield


app = FastAPI(title="Steam Oyun Analiz Asistanı", version="1.0", lifespan=yasam_dongusu)


class SoruIstegi(BaseModel):
    soru: str = Field(..., min_length=1, max_length=2000, examples=["Baldur's Gate 3'ün puanı kaç?"])
    oturum: str | None = Field(None, description="Aynı oturum = aynı sohbet hafızası. Boşsa yeni oturum açılır.")
    model: str = Field(VARSAYILAN_MODEL, examples=API_MODELLERI)


class AracCagrisi(BaseModel):
    ad: str
    argumanlar: str
    sure: float
    hata: bool
    tekrar: bool


class Cevap(BaseModel):
    cevap: str | None
    oturum: str
    model: str
    tur: int
    sure: float
    girdi_token: int
    cikti_token: int
    araclar: list[AracCagrisi]


@app.get("/saglik")
def saglik():
    return {"durum": "ok"}


@app.get("/modeller")
def modeller():
    return {"varsayilan": VARSAYILAN_MODEL, "modeller": API_MODELLERI}


@app.post("/sor", response_model=Cevap)
def sor(istek: SoruIstegi):
    if istek.model not in API_MODELLERI:
        raise HTTPException(400, f"Bilinmeyen model: {istek.model}. Seçenekler: {API_MODELLERI}")
    oturum = istek.oturum or uuid.uuid4().hex
    try:
        r = calistir(istek.soru, oturum=oturum, model=istek.model)
    except RuntimeError as e:               # ör. .env'de API anahtarı yok
        raise HTTPException(503, str(e))
    except Exception as e:                  # sağlayıcı hatası, Ollama kapalı vb.
        raise HTTPException(502, f"{type(e).__name__}: {e}")
    araclar = [AracCagrisi(ad=a["ad"], argumanlar=a["argumanlar"], sure=a["sure"],
                           hata=a.get("hata", False), tekrar=a.get("tekrar", False))
               for a in r["iz"] if a["tip"] == "arac"]
    return Cevap(cevap=r["cevap"], oturum=oturum, model=istek.model, tur=r["tur"], sure=r["sure"],
                 girdi_token=r["girdi_token"], cikti_token=r["cikti_token"], araclar=araclar)
