"""
05 – Seçilen yorumları parçalayıp Qwen3 ile vektöre çevirir ve Chroma'ya yazar.
Çalıştırma (proje klasöründe, venv açıkken):  python src/yorum_embed.py
Durdurmak: Ctrl+C. Tekrar çalıştırınca kaldığı bloktan devam eder.
"""
import json
import sqlite3
import time
from pathlib import Path

import chromadb
import numpy as np
import pandas as pd
import requests
from transformers import AutoTokenizer

DENEME = False

KOK = Path(__file__).resolve().parent.parent
DB = KOK / "data/processed/steam.db"
SECIM = KOK / "data/processed/secim_tavan200.parquet"
CHROMA_YOLU = KOK / "data/chroma"
KOLEKSIYON = "yorumlar_deneme" if DENEME else "yorumlar"
ILERLEME = CHROMA_YOLU / f"{KOLEKSIYON}_ilerleme.json"

OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL = "qwen3-embedding:4b"
BOYUT = 1024
PAKET = 32
BLOK = 2_000 if DENEME else 20_000
PARCA, ORTUSME = 512, 64


def parcala(metin, ofsetler):
    n = len(ofsetler)
    if n <= PARCA:
        return [metin]
    parcalar, bas = [], 0
    while True:
        bitis = bas + PARCA
        if n - bitis < ORTUSME:
            bitis = n
        parcalar.append(metin[ofsetler[bas][0]:ofsetler[bitis - 1][1]])
        if bitis == n:
            return parcalar
        bas = bitis - ORTUSME


def embed(metinler, deneme_sayisi=3):
    for i in range(deneme_sayisi):
        try:
            cevap = requests.post(OLLAMA_URL, json={"model": MODEL, "input": metinler}, timeout=600)
            cevap.raise_for_status()
            v = np.array(cevap.json()["embeddings"], dtype=np.float32)[:, :BOYUT]
            return v / np.linalg.norm(v, axis=1, keepdims=True)
        except Exception as hata:
            print(f"  embed hatası ({i + 1}/{deneme_sayisi}, {len(metinler)} metin): {hata}", flush=True)
            time.sleep(10)
    if len(metinler) > 1:
        orta = len(metinler) // 2
        return np.vstack([embed(metinler[:orta]), embed(metinler[orta:])])
    raise RuntimeError("Tek metin bile embed edilemedi, script durdu. Tekrar çalıştırınca devam eder.")


def main():
    satirlar = pd.read_parquet(SECIM)["satir"].sort_values().tolist()
    if DENEME:
        satirlar = satirlar[:BLOK]
    bloklar = [satirlar[i:i + BLOK] for i in range(0, len(satirlar), BLOK)]

    CHROMA_YOLU.mkdir(parents=True, exist_ok=True)
    tamamlanan = json.loads(ILERLEME.read_text())["tamamlanan_blok"] if ILERLEME.exists() else -1
    print(f"Koleksiyon: {KOLEKSIYON} | blok: {len(bloklar)} | tamamlanan: {tamamlanan + 1}", flush=True)

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    tok = AutoTokenizer.from_pretrained("BAAI/bge-m3")
    kol = chromadb.PersistentClient(path=str(CHROMA_YOLU)).get_or_create_collection(
        KOLEKSIYON, configuration={"hnsw": {"space": "cosine"}}, embedding_function=None)

    bas_genel, islenen_blok = time.time(), 0
    for b, blok in enumerate(bloklar):
        if b <= tamamlanan:
            continue
        bas = time.time()
        y = pd.read_sql(
            "SELECT review_id, app_id, olumlu, dil, tarih, faydali_oy, metin FROM yorumlar "
            f"WHERE rowid IN ({','.join(map(str, blok))})", con)
        ofsetler = tok(y["metin"].tolist(), add_special_tokens=False,
                       return_offsets_mapping=True)["offset_mapping"]

        ids, metinler, metalar = [], [], []
        for r, ofs in zip(y.itertuples(index=False), ofsetler):
            parcalar = parcala(r.metin, ofs)
            for i, p in enumerate(parcalar):
                ids.append(f"{r.review_id}#{i}")
                metinler.append(p)
                meta = {"review_id": r.review_id, "app_id": int(r.app_id), "olumlu": int(r.olumlu),
                        "dil": r.dil, "tarih": r.tarih, "faydali_oy": int(r.faydali_oy),
                        "parca_no": i, "parca_sayisi": len(parcalar)}
                metalar.append({k: v for k, v in meta.items() if v is not None})

        vektorler = np.vstack([embed(metinler[i:i + PAKET]) for i in range(0, len(metinler), PAKET)])
        for i in range(0, len(ids), 1000):
            kol.upsert(ids=ids[i:i + 1000], embeddings=vektorler[i:i + 1000],
                       documents=metinler[i:i + 1000], metadatas=metalar[i:i + 1000])
        ILERLEME.write_text(json.dumps({"tamamlanan_blok": b}))

        islenen_blok += 1
        blok_suresi = (time.time() - bas_genel) / islenen_blok
        kalan_saat = (len(bloklar) - b - 1) * blok_suresi / 3600
        print(f"[{time.strftime('%d.%m %H:%M')}] blok {b + 1}/{len(bloklar)} | {len(ids)} parça, "
              f"{time.time() - bas:.0f} sn | koleksiyon {kol.count():,} | kalan ~{kalan_saat:.1f} saat",
              flush=True)

    print("BİTTİ", flush=True)


if __name__ == "__main__":
    main()
