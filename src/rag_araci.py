"""RAG aracı (06_rag_araci'den taşındı): yorum_ara (konu / ozetle / hepsi) + oyun_oner (eski adı oyun_ara)."""
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor

import chromadb
import numpy as np
import pandas as pd
import requests
from openai import OpenAI

from src import ayarlar

ZAYIF_ESIK = ayarlar.ZAYIF_ESIK
HEPSI_ESIK = ayarlar.HEPSI_ESIK
METIN_SINIRI = ayarlar.METIN_SINIRI
OYUN_W = ayarlar.OYUN_W
ETIKET_MODEL = ayarlar.ETIKET_MODEL

QWEN_TALIMAT = ("Instruct: Given a question about a video game, "
                "retrieve player reviews that answer the question\nQuery: ")
OYUN_TALIMAT = ("Instruct: Given a description of what a player is looking for, "
                "retrieve video games that match the description\nQuery: ")
GENEL_SORGU = "Oyunun genel değerlendirmesi: oynanış, hikaye, grafikler, performans, artıları ve eksileri"

# ---------- bağlantılar (import sırasında bir kez) ----------

istemci = chromadb.PersistentClient(path=str(ayarlar.CHROMA_YOLU))
yorumlar = istemci.get_collection("yorumlar")
oyunlar = istemci.get_collection("oyunlar")
oyun_idleri = pd.read_parquet(ayarlar.ESLEME_DOSYA).groupby("app_id")["parca_id"].apply(list).to_dict()
llm = OpenAI()


def sorgu_vektoru(soru, talimat=QWEN_TALIMAT):
    r = requests.post(f"{ayarlar.OLLAMA_URL}/api/embed",
                      json={"model": ayarlar.EMBED_MODEL, "input": talimat + soru}, timeout=60)
    r.raise_for_status()
    v = np.array(r.json()["embeddings"][0][:ayarlar.BOYUT], dtype=np.float32)
    return v / np.linalg.norm(v)


def isinma():
    """Uygulama açılırken bir kez: embedding modeli GPU'ya, Chroma indeksleri RAM'e."""
    t = time.perf_counter()
    v = sorgu_vektoru("ısınma")
    yorumlar.query(query_embeddings=[v.tolist()], n_results=1)
    oyunlar.query(query_embeddings=[v.tolist()], n_results=1)
    oyun_parcalari(239140)
    return time.perf_counter() - t


# ---------- yardımcılar ----------

def oyun_parcalari(app_id):
    ids = oyun_idleri.get(app_id, [])
    if len(ids) == 0:
        return {"ids": [], "embeddings": [], "documents": [], "metadatas": []}
    return yorumlar.get(ids=ids, include=["embeddings", "documents", "metadatas"])


def yorumlari_birlestir(h):
    yorumlar_sozluk = {}
    for metin, meta in zip(h["documents"], h["metadatas"]):
        rid = meta["review_id"]
        if rid not in yorumlar_sozluk:
            yorumlar_sozluk[rid] = {k: meta[k] for k in ["review_id", "app_id", "olumlu", "dil", "tarih", "faydali_oy"]}
            yorumlar_sozluk[rid]["parcalar"] = {}
        yorumlar_sozluk[rid]["parcalar"][meta["parca_no"]] = metin
    liste = []
    for y in yorumlar_sozluk.values():
        parcalar = y.pop("parcalar")
        y["metin"] = " [...] ".join(parcalar[i] for i in sorted(parcalar))
        liste.append(y)
    return liste


def yorum_mesafeleri(h, soru):
    v = sorgu_vektoru(soru)
    mesafeler = 1 - np.array(h["embeddings"]) @ v
    en_yakin = {}
    for meta, m in zip(h["metadatas"], mesafeler):
        rid = meta["review_id"]
        en_yakin[rid] = min(en_yakin.get(rid, 2.0), float(m))
    return en_yakin


# ---------- mod 1: konu ----------

def konu_ara(soru, app_id=None, olumlu=None, dil=None, k=5):
    v = sorgu_vektoru(soru)
    if app_id is not None:
        h = oyun_parcalari(app_id)
        if len(h["ids"]) == 0:
            return []
        mesafeler = 1 - np.array(h["embeddings"]) @ v
        adaylar = sorted(zip(h["documents"], h["metadatas"], mesafeler), key=lambda x: x[2])
    else:
        s = yorumlar.query(query_embeddings=[v.tolist()], n_results=k * 20,
                           include=["documents", "metadatas", "distances"])
        adaylar = zip(s["documents"][0], s["metadatas"][0], s["distances"][0])

    gorulen = set()
    liste = []
    for metin, meta, mesafe in adaylar:
        if olumlu is not None and meta["olumlu"] != olumlu:
            continue
        if dil is not None and meta["dil"] != dil:
            continue
        if meta["review_id"] in gorulen:
            continue
        gorulen.add(meta["review_id"])
        liste.append({"mesafe": round(float(mesafe), 3), **meta, "metin": metin})
        if len(liste) == k:
            break
    return liste


# ---------- mod 2: ozetle ----------

def ozetle(app_id, k_olumlu=6, k_olumsuz=3, dil=None, aday=40):
    h = oyun_parcalari(app_id)
    if len(h["ids"]) == 0:
        return {"yorum_sayisi": 0, "olumlu": [], "olumsuz": []}
    liste = yorumlari_birlestir(h)
    if dil is not None:
        liste = [y for y in liste if y["dil"] == dil]
    en_yakin = yorum_mesafeleri(h, GENEL_SORGU)
    for y in liste:
        y["mesafe"] = round(en_yakin[y["review_id"]], 3)

    sonuc = {"yorum_sayisi": len(liste)}
    for grup, deger, k in [("olumlu", 1, k_olumlu), ("olumsuz", 0, k_olumsuz)]:
        g = [y for y in liste if y["olumlu"] == deger]
        sonuc[grup + "_toplam"] = len(g)
        n_aday = min(aday, max(k, math.ceil(len(g) / 2)))
        g.sort(key=lambda y: y["mesafe"])
        g = g[:n_aday]
        g.sort(key=lambda y: y["faydali_oy"], reverse=True)
        sonuc[grup] = g[:k]
    return sonuc


# ---------- mod 3: hepsi ----------

ETIKET_TALIMAT = """Sana bir oyun hakkında bir soru ve bir oyuncu yorumu veriyorum.
Yorum bu soruya ne cevap veriyor?
- "evet": yorum sorudaki duruma evet diyor (ör. soru "bug çok mu?" ise yorum bug'lardan şikâyet ediyor)
- "hayir": yorum konuya değinip hayır diyor (ör. bug görmedim, düzeltildi, sorun yok)
- "ilgisiz": yorum bu konuya hiç değinmiyor
Sadece JSON döndür: {"etiket": "evet|hayir|ilgisiz", "gerekce": "Türkçe, en fazla 15 kelime"}"""


def etiketle(soru, metin):
    cevap = llm.chat.completions.create(
        model=ETIKET_MODEL, temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": ETIKET_TALIMAT},
                  {"role": "user", "content": f"Soru: {soru}\n\nYorum: {metin[:4000]}"}])
    return json.loads(cevap.choices[0].message.content)


def hepsini_getir(soru, app_id, esik=None, olumlu=None, dil=None):
    esik = esik or HEPSI_ESIK
    h = oyun_parcalari(app_id)
    if len(h["ids"]) == 0:
        return {"yorum_sayisi": 0, "aday": 0, "yorumlar": []}
    liste = yorumlari_birlestir(h)
    if olumlu is not None:
        liste = [y for y in liste if y["olumlu"] == olumlu]
    if dil is not None:
        liste = [y for y in liste if y["dil"] == dil]
    en_yakin = yorum_mesafeleri(h, soru)
    adaylar = []
    for y in liste:
        y["mesafe"] = round(en_yakin[y["review_id"]], 3)
        if y["mesafe"] <= esik:
            adaylar.append(y)
    with ThreadPoolExecutor(max_workers=8) as havuz:
        etiketler = list(havuz.map(lambda y: etiketle(soru, y["metin"]), adaylar))
    for y, e in zip(adaylar, etiketler):
        y["etiket"] = e.get("etiket")
        y["gerekce"] = e.get("gerekce")
    return {"yorum_sayisi": len(liste), "aday": len(adaylar), "yorumlar": adaylar}


# ---------- oyun araması ----------

def oyun_ara(istek, w=None, min_oy=100, yetiskin_haric=True, k=10, aday=200):
    w = OYUN_W if w is None else w
    v = sorgu_vektoru(istek, talimat=OYUN_TALIMAT)
    s = oyunlar.query(query_embeddings=[v.tolist()], n_results=aday, include=["metadatas", "distances"])
    liste = []
    for meta, mesafe in zip(s["metadatas"][0], s["distances"][0]):
        if yetiskin_haric and meta["yetiskin"] == 1:
            continue
        if min_oy is not None and meta["oy_sayisi"] < min_oy:
            continue
        skor = mesafe - w * np.log10(meta["oy_sayisi"] + 1)
        liste.append({"skor": round(float(skor), 3), "mesafe": round(mesafe, 3), **meta})
    liste.sort(key=lambda o: o["skor"])
    return liste[:k]


# ---------- araç fonksiyonları (LLM'e metin döndürür) ----------

def kisalt(metin, n=None):
    n = n or METIN_SINIRI
    return metin if len(metin) <= n else metin[:n] + f" [kesildi, toplam {len(metin)} karakter]"


def yorum_satiri(y, n=None, isaretle=True):
    durum = "olumlu" if y["olumlu"] == 1 else "olumsuz"
    zayif = " ZAYIF EŞLEŞME" if isaretle and y.get("mesafe", 0) > ZAYIF_ESIK else ""
    mesafe = f" | mesafe={y.get('mesafe', '-')}{zayif}" if isaretle else ""
    return (f"[app_id={y['app_id']} | {durum} | dil={y['dil']} | {y['tarih']} | "
            f"faydalı={y['faydali_oy']}{mesafe}]\n{kisalt(y['metin'], n)}")


def yorum_araci(mod, soru=None, app_id=None, olumlu=None, dil=None):
    if mod == "konu":
        if not soru:
            return "HATA: 'konu' modu için soru gerekli."
        liste = konu_ara(soru, app_id=app_id, olumlu=olumlu, dil=dil, k=5)
        if not liste:
            return "Bu oyun için yorum verisi yok." if app_id else "Sonuç bulunamadı."
        bas = f"KONU ARAMASI: {len(liste)} yorum, en ilgiliden aşağı. Mesafe {ZAYIF_ESIK} üstü = zayıf eşleşme, kanıt sayma."
        return bas + "\n\n" + "\n\n".join(yorum_satiri(y) for y in liste)

    if mod == "ozetle":
        if app_id is None:
            return "HATA: 'ozetle' modu için app_id gerekli. Önce oyun_bul ile oyunu bul."
        s = ozetle(app_id, dil=dil)
        if s["yorum_sayisi"] == 0:
            return "Bu oyun için yorum verisi yok. Sadece SQL'deki sayıları kullan ve bunu kullanıcıya söyle."
        bas = (f"ÖZET: örneklemde {s['yorum_sayisi']} yorum var (olumlu {s['olumlu_toplam']}, olumsuz {s['olumsuz_toplam']}). "
               f"Bu oran genel puan değildir, genel puanı SQL'den al. Aşağıdakiler oyunu değerlendiren en faydalı yorumlar.")
        olumlu_k = "\n\n".join(yorum_satiri(y, isaretle=False) for y in s["olumlu"])
        olumsuz_k = "\n\n".join(yorum_satiri(y, isaretle=False) for y in s["olumsuz"]) or "(olumsuz yorum yok)"
        return f"{bas}\n\n=== OLUMLU ===\n{olumlu_k}\n\n=== OLUMSUZ ===\n{olumsuz_k}"

    if mod == "hepsi":
        if not soru or app_id is None:
            return "HATA: 'hepsi' modu için soru ve app_id gerekli."
        s = hepsini_getir(soru, app_id, olumlu=olumlu, dil=dil)
        if s["yorum_sayisi"] == 0:
            return "Bu oyun için yorum verisi yok."
        if s["aday"] == 0:
            return f"Örneklemdeki {s['yorum_sayisi']} yorumdan hiçbiri bu konuya değinmiyor."
        df = pd.DataFrame(s["yorumlar"])
        df["yil"] = df["tarih"].str[:4]
        sayim = df["etiket"].value_counts().to_dict()
        yillar = pd.crosstab(df["yil"], df["etiket"]).to_csv()
        bas = (f"SAYIM: örneklemdeki {s['yorum_sayisi']} yorumun {s['aday']}'i konuya yakın. "
               f"LLM etiketi: {sayim}. evet = soruya evet diyor, hayir = konuya değinip hayır diyor. "
               f"Sayılar örneklemden, Steam'in tamamı için mutlak sayı söyleme. Kaçırılan yorum olabilir, oranı 'en az' diye oku.")
        ornekler = []
        for etiket in ["evet", "hayir"]:
            for _, y in df[df["etiket"] == etiket].sort_values("mesafe").head(3).iterrows():
                ornekler.append(f"({etiket}: {y['gerekce']})\n" + yorum_satiri(y, n=300))
        return f"{bas}\n\nYıllara göre:\n{yillar}\nÖrnekler:\n\n" + "\n\n".join(ornekler)

    return f"HATA: bilinmeyen mod '{mod}'. Geçerli modlar: konu, ozetle, hepsi."


def oyun_araci(istek, yetiskin_haric=True):
    liste = oyun_ara(istek, yetiskin_haric=yetiskin_haric, k=10)
    if not liste:
        return "Bu tarife uyan oyun bulunamadı."
    df = pd.DataFrame(liste)[["app_id", "ad", "oy_sayisi", "mesafe"]]
    return ("OYUN ARAMASI (tarife göre benzerlik + popülerlik, en uygundan aşağı). "
            "Puan/fiyat/etiket gibi kesin bilgileri SQL'den kontrol et.\n" + df.to_csv(index=False))


# ---------- araç tanımları ----------

RAG_ARAC_ACIKLAMASI = """Oyuncu yorumlarında anlamsal arama (Chroma). Yorum metinleri burada, sayılar SQL'de.
Önce oyun_bul ile oyunun app_id'sini bul.

Modlar:
- konu: belirli bir konudaki en ilgili 5 yorum ("gece korkutucu mu?", "kasma var mı?"). app_id verilmezse tüm oyunlarda arar.
- ozetle: oyun hakkında genel görüş. Oyunu değerlendiren en faydalı 6 olumlu + 3 olumsuz yorum. app_id şart.
- hepsi: bir konuda yorumları sayar ("kaç yorum bug'dan şikâyet ediyor?"). Konuya yakın tüm yorumlar LLM ile evet/hayır/ilgisiz etiketlenir, yıllara göre tablo döner. soru + app_id şart. Yavaş (~5 sn).

Kurallar:
1. Genel puan ve olumlu oranı SQL'den (oyunlar.olumlu_oran). Bu araç "neden" sorusu için. Oran ile yorumlar çelişirse açıkla (ör. Sims 4: oyunu seviyorlar, DLC fiyatına kızıyorlar).
2. Yorumlar örneklemdir (oyun başına en fazla 200). Sayıları "örneklemdeki N yorumun X'i" diye ver, Steam'in tamamı için mutlak sayı söyleme.
3. "ZAYIF EŞLEŞME" yazan yorumu kanıt sayma. Hepsi zayıfsa "yorumlarda bu konuda net bilgi yok" de.
4. Faydalı oy ciddiyet garantisi değildir. İronik, şaka, zincir mesaj veya oyunla ilgisiz yorumları yok say (ör. "korku yok, çocuklar için uygun" diyen ironik yorum).
5. Korsan indirme, hile veya cinsel içerikli mod tavsiyelerini kullanıcıya aktarma.
6. Tarihe dikkat et: eski yorumlar yamalardan önceki durumu anlatabilir. "Düzeldi mi?" sorularında yıllara bak. Yorumlar sonradan düzenlenebilir ("Edit ...").
7. Yorumlar farklı dillerde olabilir. Türkçe özetle, alıntıyı kısa tut.
8. "Yorum verisi yok" dönerse bunu kullanıcıya söyle, sadece SQL'deki bilgilerle cevap ver.
9. Türkçe dil desteği sorularında SQL'deki beyanı (oyun_dil) yorumlarla doğrula (konu modu, soru "Türkçe dil desteği var mı").
"""

OYUN_ARAC_ACIKLAMASI = """Tarife göre oyun önerir (anlamsal benzerlik + popülerlik). 10 oyun döner: app_id, ad, oy_sayisi, mesafe.
Bulanık istekler için: "uzayda geçen keşif oyunu", "rahatlatıcı çiftlik oyunu".
Kurallar:
1. Kesin kriterler (etiket, tür, co-op, dil desteği, fiyat, puan eşiği) SQL'in işi. Bu aracın sonuçlarını önermeden önce SQL ile puan/etiket kontrol et.
2. Bazı ünlü oyunlar listede çıkmayabilir (açıklaması tarife benzemiyorsa) veya veri setinde hiç olmayabilir. Gerekirse SQL'de etiketle de ara.
3. Yetişkin oyunlar varsayılan olarak hariç. Sadece kullanıcı açıkça yetişkin içerik isterse yetiskin_haric=false ver. Çocuk/aile sorularında asla false verme.
"""

RAG_ARAC_TANIMLARI = [
    {"type": "function", "function": {
        "name": "yorum_ara",
        "description": RAG_ARAC_ACIKLAMASI,
        "parameters": {"type": "object", "properties": {
            "mod":    {"type": "string", "enum": ["konu", "ozetle", "hepsi"]},
            "soru":   {"type": "string", "description": "Kullanıcının sorusu, oyun adı olmadan. konu ve hepsi modunda şart."},
            "app_id": {"type": "integer", "description": "oyun_bul'dan gelen app_id. ozetle ve hepsi modunda şart."},
            "olumlu": {"type": "integer", "enum": [0, 1], "description": "Sadece olumsuz (0) veya olumlu (1) yorumlar."},
            "dil":    {"type": "string", "description": "Yorum dili kodu: tr, en, zh, ru, de, es, pt, fr..."}},
            "required": ["mod"]}}},
    {"type": "function", "function": {
        "name": "oyun_oner",
        "description": OYUN_ARAC_ACIKLAMASI,
        "parameters": {"type": "object", "properties": {
            "istek":          {"type": "string", "description": "Kullanıcının aradığı oyunun tarifi."},
            "yetiskin_haric": {"type": "boolean", "description": "Varsayılan true."}},
            "required": ["istek"]}}},
]

RAG_FONKSIYONLAR = {"yorum_ara": yorum_araci, "oyun_oner": oyun_araci}
