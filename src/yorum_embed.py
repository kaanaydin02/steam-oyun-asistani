"""
05 – Seçilen yorumları parçalayıp Qwen3 ile vektöre çevirir ve blok blok DOSYAYA kaydeder.
Chroma'ya yükleme ayrı ve tek seferlik bir adım. Pencere/PC ne zaman kapanırsa kapansın
en fazla o an işlenen blok kaybolur.
Çalıştırma: masaüstündeki "Embedding Baslat.bat"
"""
import sqlite3
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from transformers import AutoTokenizer

KOK = Path(__file__).resolve().parent.parent
DB = KOK / "data/processed/steam.db"
SECIM = KOK / "data/processed/secim_tavan200.parquet"
CIKTI = KOK / "data/vektorler/yorumlar"
BASLANGIC_BLOK = 51   # 0–50 eski Chroma'da. Kurtarılamazsa 0 yapılacak.

OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL = "qwen3-embedding:4b"
BOYUT = 1024
PAKET = 32
BLOK = 20_000
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


def ollama_istek(metinler):
    cevap = requests.post(OLLAMA_URL, json={"model": MODEL, "input": metinler}, timeout=600)
    if cevap.status_code != 200:
        raise RuntimeError(f"{cevap.status_code}: {cevap.text[:300]}")
    v = np.array(cevap.json()["embeddings"], dtype=np.float32)[:, :BOYUT]
    if not np.isfinite(v).all():
        raise RuntimeError("bozuk (NaN) vektör")
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def embed(metinler):
    """Her metin için bir vektör ya da None (atlandı) döndürür."""
    for _ in range(3):
        try:
            return list(ollama_istek(metinler))
        except requests.ConnectionError:
            print("  Ollama'ya bağlanılamadı, 30 sn sonra tekrar denenecek...", flush=True)
            time.sleep(30)
        except RuntimeError as hata:
            if len(metinler) == 1:
                print(f"  ATLANDI (1 metin, {len(metinler[0])} kar.): {hata}", flush=True)
                return [None]
            orta = len(metinler) // 2
            return embed(metinler[:orta]) + embed(metinler[orta:])
    raise SystemExit("Ollama çalışmıyor. Ollama'yı açıp tekrar başlat.")


def main():
    satirlar = pd.read_parquet(SECIM)["satir"].sort_values().tolist()
    bloklar = [satirlar[i:i + BLOK] for i in range(0, len(satirlar), BLOK)]
    CIKTI.mkdir(parents=True, exist_ok=True)
    yapilacak = [b for b in range(BASLANGIC_BLOK, len(bloklar))
                 if not (CIKTI / f"blok_{b:03d}.npy").exists()]
    print(f"Toplam blok: {len(bloklar)} | bu çalıştırmada yapılacak: {len(yapilacak)}", flush=True)

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    tok = AutoTokenizer.from_pretrained("BAAI/bge-m3")

    bas_genel = time.time()
    for sayac, b in enumerate(yapilacak, start=1):
        bas = time.time()
        y = pd.read_sql(
            "SELECT review_id, app_id, olumlu, dil, tarih, faydali_oy, metin FROM yorumlar "
            f"WHERE rowid IN ({','.join(map(str, bloklar[b]))})", con)
        ofsetler = tok(y["metin"].tolist(), add_special_tokens=False,
                       return_offsets_mapping=True)["offset_mapping"]

        kayitlar = []
        for r, ofs in zip(y.itertuples(index=False), ofsetler):
            parcalar = parcala(r.metin, ofs)
            for i, p in enumerate(parcalar):
                kayitlar.append({"parca_id": f"{r.review_id}#{i}", "review_id": r.review_id,
                                 "app_id": int(r.app_id), "olumlu": int(r.olumlu), "dil": r.dil,
                                 "tarih": r.tarih, "faydali_oy": int(r.faydali_oy),
                                 "parca_no": i, "parca_sayisi": len(parcalar), "metin": p})
        tablo = pd.DataFrame(kayitlar)
        metinler = tablo["metin"].tolist()

        vektorler = []
        for i in range(0, len(metinler), PAKET):
            vektorler += embed(metinler[i:i + PAKET])
        tamam = np.array([v is not None for v in vektorler])
        tablo["atlandi"] = ~tamam
        vektor_tablosu = np.vstack([v for v in vektorler if v is not None])

        tablo.to_parquet(CIKTI / f"blok_{b:03d}.parquet", index=False)
        gecici = CIKTI / f"blok_{b:03d}.tmp.npy"
        np.save(gecici, vektor_tablosu)
        gecici.rename(CIKTI / f"blok_{b:03d}.npy")

        ort = (time.time() - bas_genel) / sayac
        kalan = (len(yapilacak) - sayac) * ort / 3600
        print(f"[{time.strftime('%d.%m %H:%M')}] blok {b + 1}/{len(bloklar)} | {tamam.sum()} parça "
              f"(atlanan {(~tamam).sum()}), {time.time() - bas:.0f} sn | kalan ~{kalan:.1f} saat",
              flush=True)

    print("BİTTİ", flush=True)


if __name__ == "__main__":
    main()
