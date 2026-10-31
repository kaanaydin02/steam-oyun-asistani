"""Oyun koleksiyonu: oyun metinlerini embed eder, dosyaya yazar, sonra Chroma'ya yükler."""
import sqlite3, time
from pathlib import Path
import numpy as np, pandas as pd, requests, chromadb

KOK = Path(__file__).resolve().parents[1]
DB = KOK / "data/processed/steam.db"
CIKTI = KOK / "data/vektorler/oyunlar"
CHROMA = KOK / "data/chroma_v2"
MODEL = "qwen3-embedding:4b"
OLLAMA = "http://localhost:11434"
BOYUT, PAKET, BLOK = 1024, 16, 1000
QWEN_TALIMAT = "Instruct: Given a question about a video game, retrieve player reviews that answer the question\nQuery: "


def metin_mi(x):
    return isinstance(x, str) and x.strip() != ""


def oyun_metni(r):
    parcalar = [r.ad]
    if metin_mi(r.kisa_aciklama):
        parcalar.append(r.kisa_aciklama.strip())
    if metin_mi(r.oyun_hakkinda):
        parcalar.append(r.oyun_hakkinda.strip()[:2000])
    if metin_mi(r.etiketler):
        parcalar.append("Etiketler: " + r.etiketler)
    return "\n".join(parcalar)


def oyunlari_oku():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    oyun = pd.read_sql("""SELECT app_id, ad, kisa_aciklama, oyun_hakkinda, yorum_var, oy_sayisi, yetiskin
                          FROM oyunlar WHERE yorum_var = 1 OR oy_sayisi >= 100 ORDER BY app_id""", con)
    etiket = pd.read_sql("SELECT app_id, etiket, sira FROM oyun_etiket", con)
    con.close()
    ilk10 = (etiket.sort_values(["app_id", "sira"]).groupby("app_id").head(10)
             .groupby("app_id")["etiket"].agg(", ".join).rename("etiketler"))
    oyun = oyun.merge(ilk10, on="app_id", how="left")
    oyun["metin"] = [oyun_metni(r) for r in oyun.itertuples()]
    for s in ["yorum_var", "oy_sayisi", "yetiskin"]:
        oyun[s] = oyun[s].fillna(0).astype(int)
    return oyun[["app_id", "ad", "yorum_var", "oy_sayisi", "yetiskin", "etiketler", "metin"]]


def ollama_istek(metinler):
    r = requests.post(f"{OLLAMA}/api/embed", timeout=600,
                      json={"model": MODEL, "input": metinler, "options": {"num_ctx": 4096}})
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}: {r.text[:300]}")
    v = np.asarray(r.json()["embeddings"], dtype=np.float32)[:, :BOYUT]
    if np.isnan(v).any():
        raise RuntimeError("NaN vektör")
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def embed(metinler):
    try:
        return ollama_istek(metinler)
    except RuntimeError as hata:
        if len(metinler) == 1:
            raise
        print("  paket bölünüyor:", hata, flush=True)
        yari = len(metinler) // 2
        return np.vstack([embed(metinler[:yari]), embed(metinler[yari:])])


def gpu_kontrol():
    embed(["ısınma"])
    modeller = requests.get(f"{OLLAMA}/api/ps").json()["models"]
    vram = [m.get("size_vram", 0) for m in modeller if m["name"].startswith(MODEL)]
    if not vram or vram[0] == 0:
        raise SystemExit("Ollama GPU'da DEĞİL (size_vram 0). Ollama'yı Quit edip yeniden aç, sonra tekrar çalıştır.")
    print(f"GPU tamam: {vram[0] / 1e9:.1f} GB VRAM'de")


def main():
    gpu_kontrol()
    CIKTI.mkdir(parents=True, exist_ok=True)
    oyun = oyunlari_oku()
    oyun.to_parquet(CIKTI / "oyunlar.parquet", index=False)
    baslar = list(range(0, len(oyun), BLOK))
    print(f"oyun: {len(oyun)} | blok: {len(baslar)}", flush=True)

    bas = time.time()
    for no, i in enumerate(baslar):
        hedef = CIKTI / f"blok_{no:03d}.npy"
        if hedef.exists():
            continue
        metinler = oyun["metin"].iloc[i:i + BLOK].tolist()
        vek = np.vstack([embed(metinler[j:j + PAKET]) for j in range(0, len(metinler), PAKET)])
        gecici = CIKTI / f"blok_{no:03d}.tmp.npy"
        np.save(gecici, vek)
        gecici.rename(hedef)
        print(f"blok {no + 1}/{len(baslar)} | geçen {(time.time() - bas) / 60:.1f} dk", flush=True)

    vek = np.vstack([np.load(CIKTI / f"blok_{no:03d}.npy") for no in range(len(baslar))])
    assert len(vek) == len(oyun), (len(vek), len(oyun))

    print("Chroma'ya yükleniyor, KAPATMA...", flush=True)
    client = chromadb.PersistentClient(path=str(CHROMA))
    kol = client.get_or_create_collection("oyunlar", embedding_function=None,
                                          configuration={"hnsw": {"space": "cosine"}})
    meta = oyun[["app_id", "ad", "yorum_var", "oy_sayisi", "yetiskin"]].to_dict("records")
    paket = client.get_max_batch_size()
    for i in range(0, len(oyun), paket):
        kol.upsert(ids=oyun["app_id"].iloc[i:i + paket].astype(str).tolist(),
                   embeddings=vek[i:i + paket],
                   documents=oyun["metin"].iloc[i:i + paket].tolist(),
                   metadatas=meta[i:i + paket])
    print("count:", kol.count(), "| beklenen:", len(oyun))

    soru = "uzayda geçen, gezegen keşfedilen açık dünya rol yapma oyunu"
    sonuc = kol.query(query_embeddings=embed([QWEN_TALIMAT + soru]), n_results=5)
    print("test:", soru)
    for m, d in zip(sonuc["metadatas"][0], sonuc["distances"][0]):
        print(f"  {d:.3f}  {m['ad']}  (oy {m['oy_sayisi']})")


if __name__ == "__main__":
    main()
