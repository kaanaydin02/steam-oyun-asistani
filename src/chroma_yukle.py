"""Vektör dosyalarını (kurtarilan_* + blok_*) yeni Chroma koleksiyonuna yükler."""
import json, os, time
from pathlib import Path
import numpy as np, pandas as pd, chromadb

KOK = Path(__file__).resolve().parents[1]
KLASOR = KOK / "data/vektorler/yorumlar"
CHROMA = KOK / "data/chroma_v2"
KOLEKSIYON = "yorumlar"
ILERLEME = CHROMA / "yukleme_ilerleme.json"
BEKLENEN = 2_644_490
METADATA = ["review_id", "app_id", "olumlu", "dil", "tarih",
            "faydali_oy", "parca_no", "parca_sayisi"]
SAYI = ["app_id", "olumlu", "faydali_oy", "parca_no", "parca_sayisi"]


def main():
    ram = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1e9
    print(f"WSL RAM: {ram:.1f} GB | vektörlerin boyu: {BEKLENEN * 1024 * 4 / 1e9:.1f} GB")

    dosyalar = sorted(KLASOR.glob("kurtarilan_*.parquet")) + sorted(KLASOR.glob("blok_*.parquet"))
    CHROMA.mkdir(parents=True, exist_ok=True)
    biten = set(json.loads(ILERLEME.read_text())) if ILERLEME.exists() else set()

    client = chromadb.PersistentClient(path=str(CHROMA))
    kol = client.get_or_create_collection(
        KOLEKSIYON, embedding_function=None,
        configuration={"hnsw": {"space": "cosine"}})
    paket = client.get_max_batch_size()
    print(f"dosya: {len(dosyalar)} | biten: {len(biten)} | paket: {paket} | şu anki count: {kol.count()}")

    bas = time.time()
    for n, dosya in enumerate(dosyalar, 1):
        if dosya.name in biten:
            continue
        tablo = pd.read_parquet(dosya)
        tablo = tablo[~tablo["atlandi"]].reset_index(drop=True)
        vek = np.load(dosya.with_suffix(".npy"))
        assert len(tablo) == len(vek), dosya.name
        tablo[SAYI] = tablo[SAYI].astype(int)
        tablo["review_id"] = tablo["review_id"].astype(str)
        tablo["dil"] = tablo["dil"].astype(str)
        tablo["tarih"] = tablo["tarih"].astype(str)
        meta = tablo[METADATA].to_dict("records")

        for i in range(0, len(tablo), paket):
            kol.upsert(ids=tablo["parca_id"].iloc[i:i + paket].tolist(),
                       embeddings=vek[i:i + paket],
                       documents=tablo["metin"].iloc[i:i + paket].tolist(),
                       metadatas=meta[i:i + paket])

        biten.add(dosya.name)
        ILERLEME.write_text(json.dumps(sorted(biten)))
        print(f"{n}/{len(dosyalar)} {dosya.name}: {len(tablo)} parça | "
              f"geçen süre {(time.time() - bas) / 60:.1f} dk", flush=True)

    toplam = kol.count()
    print("count:", toplam, "| beklenen:", BEKLENEN, "| fark:", toplam - BEKLENEN)
    ornek = kol.get(limit=1, include=["embeddings", "metadatas"])
    sonuc = kol.query(query_embeddings=ornek["embeddings"], n_results=3)
    print("örnek metadata:", ornek["metadatas"][0])
    print("test:", ornek["ids"][0], "→", sonuc["ids"][0], sonuc["distances"][0])


if __name__ == "__main__":
    main()
