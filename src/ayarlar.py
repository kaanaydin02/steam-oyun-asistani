"""Projenin bütün yolları ve ayarları tek yerde."""
import os
from pathlib import Path

from dotenv import load_dotenv

KOK = Path(__file__).resolve().parent.parent
load_dotenv(KOK / ".env")

# Veri dosyaları
DB_YOLU = KOK / "data" / "processed" / "steam.db"
CHROMA_YOLU = KOK / "data" / "chroma_v2"
ESLEME_DOSYA = KOK / "data" / "processed" / "chroma_parca_esleme.parquet"

# SQL aracı (04)
SATIR_SINIRI = 50
ZAMAN_ASIMI_SN = 10
METIN_MODU = "gizle"   # "gizle" veya "kes"
KESME_UZUNLUGU = 200

# RAG aracı (05-06)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = "qwen3-embedding:4b"
BOYUT = 1024
ZAYIF_ESIK = 0.45
HEPSI_ESIK = 0.45
METIN_SINIRI = 1200
OYUN_W = 0.03
ETIKET_MODEL = "deepseek-flash"
