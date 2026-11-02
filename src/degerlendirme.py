"""Değerlendirme (08-09): soru setini çalıştırma, otomatik kontroller ve LLM hakem tek yerde."""
import json
import re
from datetime import datetime

import pandas as pd
from tqdm.auto import tqdm

from src import ayarlar, llm
from src.agent_graf import GRAF, calistir
from src.araclar import ARAC_TANIMLARI
from src.talimat import SISTEM_TALIMATI

# ---------------------------------------------------------------- dosyalar ve sabitler
RAPOR = ayarlar.KOK / "reports"
SORU_DOSYA = RAPOR / "08_soru_seti.json"
SONUC_DOSYA = RAPOR / "08_calistirmalar.jsonl"      # 08 ve 09 çalıştırmaları aynı dosyada
HAKEM_DOSYA = RAPOR / "08_hakem.jsonl"
HAKEM_TALIMAT_DOSYA = RAPOR / "hakem_talimati_v3.txt"

SORULAR = json.loads(SORU_DOSYA.read_text(encoding="utf-8"))
SORU = {s["id"]: s for s in SORULAR}
BEKLENEN = {s["id"]: s["beklenen_arac"] for s in SORULAR}
YASAK = {"D3": ["oyun_bul"]}            # hafıza sorusunda oyunu tekrar aramamalı
ESKI_AD = {"oyun_oner": "oyun_ara"}     # soru setinde beklenen araç eski adla yazılı

# $ / 1 milyon token: (girdi, çıktı)
FIYAT = {
    "gpt-4.1-mini":   (0.40, 1.60),
    "gpt-6-luna":     (0.10, 0.50),     # 3. taraf sitelerden
    "deepseek-flash": (0.15, 0.60),     # resmî, yoğun olmayan saat + önbelleksiz girdi
    "qwen2.5:7b":     (0.0, 0.0),       # yerel: elektrik hariç bedava
    "gpt-6.1-terra":  (2.00, 10.00),    # YER TUTUCU (hakem)
}

HAKEM_MODEL, HAKEM_SURUM = "gpt-6.1-terra", "v3"
ANAHTAR = ["id", "model", "tekrar", "metin_modu", "deney"]


def jsonl_oku(yol):
    if not yol.exists():
        return []
    with open(yol, encoding="utf-8") as f:
        return [json.loads(s) for s in f if s.strip()]


def jsonl_ekle(yol, kayit):
    with open(yol, "a", encoding="utf-8") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- 1) çalıştırma
def yapilanlar():
    return {(k["id"], k["tekrar"], k["model"], k["metin_modu"], k.get("deney", "v4")) for k in jsonl_oku(SONUC_DOSYA)}


def arac_ciktilari(oturum):
    mesajlar = GRAF.get_state({"configurable": {"thread_id": oturum}}).values["mesajlar"]
    return [m["content"] for m in mesajlar if m.get("role") == "tool"]


def bir_calistirma(s, tekrar, model, deney):
    oturum = f"09-{model}-{s['id']}-{tekrar}-{datetime.now():%H%M%S%f}"
    if s["onceki"]:
        calistir(s["onceki"], oturum=oturum, model=model)
    r = calistir(s["soru"], oturum=oturum, model=model)
    gf, cf = FIYAT[model]
    return {"id": s["id"], "kategori": s["kategori"], "tekrar": tekrar, "model": model,
            "metin_modu": ayarlar.METIN_MODU, "deney": deney, "talimat_kar": len(SISTEM_TALIMATI),
            "soru": s["soru"], "cevap": r["cevap"],
            "arac_adlari": [a["ad"] for a in r["iz"] if a["tip"] == "arac"], "araclar": r["araclar"],
            "arac_hata": sum(a.get("hata", False) for a in r["iz"]),
            "tekrar_engel": sum(a.get("tekrar", False) for a in r["iz"]),
            "tur": r["tur"], "sure": r["sure"], "girdi_token": r["girdi_token"], "cikti_token": r["cikti_token"],
            "maliyet_usd": round((r["girdi_token"] * gf + r["cikti_token"] * cf) / 1e6, 5),
            "arac_ciktilari": arac_ciktilari(oturum),
            "zaman": datetime.now().isoformat(timespec="seconds"), "hata": None}


def hepsini_calistir(model, tekrarlar=(1, 2, 3), deney="v5"):
    """Eksik (soru, tekrar) çiftlerini çalıştırır; biten kayıtlara dokunmaz, yarıda kalırsa kaldığı yerden devam eder."""
    bitti = yapilanlar()
    isler = [(s, t) for t in tekrarlar for s in SORULAR
             if (s["id"], t, model, ayarlar.METIN_MODU, deney) not in bitti]
    print(f"{model} · deney {deney} · {ayarlar.METIN_MODU} · yapılacak: {len(isler)}")
    for s, t in tqdm(isler, desc=model):
        try:
            kayit = bir_calistirma(s, t, model, deney)
        except Exception as e:
            kayit = {"id": s["id"], "kategori": s["kategori"], "tekrar": t, "model": model,
                     "metin_modu": ayarlar.METIN_MODU, "deney": deney, "soru": s["soru"], "cevap": None,
                     "zaman": datetime.now().isoformat(timespec="seconds"), "hata": f"{type(e).__name__}: {e}"}
        jsonl_ekle(SONUC_DOSYA, kayit)


def sonuclar():
    df = pd.DataFrame(jsonl_oku(SONUC_DOSYA))
    df["deney"] = df["deney"].fillna("v4")
    for sutun in ["tekrar_engel", "arac_hata"]:
        df[sutun] = df[sutun].fillna(0)
    return df


# ---------------------------------------------------------------- 2) otomatik kontroller
def ciktilar(r):
    return r["arac_ciktilari"] if isinstance(r["arac_ciktilari"], list) else []


def arac_dogru(r):
    cagrilan = {ESKI_AD.get(a, a) for a in (r["arac_adlari"] if isinstance(r["arac_adlari"], list) else [])}
    bek = BEKLENEN[r["id"]]
    if not bek:
        return len(cagrilan) == 0
    return set(bek) <= cagrilan and not (cagrilan & set(YASAK.get(r["id"], [])))


def tr_sayi(ham):
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", ham):
        ham = ham.replace(".", "")
    try:
        return float(ham.replace(",", "."))
    except ValueError:
        return None


SAYI_EN = r"\d+(?:\.\d+)?"
SABIT_HAVUZ = {float(x) for x in re.findall(SAYI_EN, SISTEM_TALIMATI + json.dumps(ARAC_TANIMLARI, ensure_ascii=False))}


def yakin(v, h):
    if abs(v - h) < 1e-9 or abs(v / 100 - h) <= 0.0051:
        return True
    return h > 0 and any(abs(v * carpan - h) <= 0.005 * h for carpan in (1, 1_000, 1_000_000))


def supheli_sayilar(r):
    havuz = SABIT_HAVUZ | {float(x) for c in ciktilar(r) + [r["soru"]] for x in re.findall(SAYI_EN, c)}
    supheli = []
    cevap = r["cevap"] if isinstance(r["cevap"], str) else ""
    for ham in re.findall(r"\d+(?:[.,]\d+)*", cevap):
        v = tr_sayi(ham)
        if v is None or (v.is_integer() and v <= 10):
            continue
        if not any(yakin(v, h) for h in havuz):
            supheli.append(ham)
    return supheli


def kontrolleri_ekle(df):
    df = df.copy()
    df["arac_dogru"] = df.apply(arac_dogru, axis=1)
    df["supheli"] = df.apply(supheli_sayilar, axis=1)
    df["supheli_var"] = df["supheli"].str.len() > 0
    df["arac_hatali"] = df.apply(lambda r: any(c.startswith("HATA") for c in ciktilar(r)), axis=1)
    return df


# ---------------------------------------------------------------- 3) LLM hakem
def hakem_talimati():
    return HAKEM_TALIMAT_DOSYA.read_text(encoding="utf-8")


def hakem_mesaji(r, kirp=15000):
    s = SORU[r["id"]]
    son_ciktilar = ciktilar(r)[-len(r["araclar"]):] if r["araclar"] else []
    cagri_cikti = "\n\n".join(f"--- {c}\n{o[:kirp]}" for c, o in zip(r["araclar"], son_ciktilar))
    on = f"(Aynı oturumda önce şu soruldu: {s['onceki']})\n" if s["onceki"] else ""
    return (f"SORU: {on}{s['soru']}\n\nKONTROL: {s['kontrol']}\nBEKLENEN ARAÇLAR: {s['beklenen_arac']}\n\n"
            f"REFERANS:\n{s['referans_metin'] or '(yok)'}\n\n"
            f"AGENT'IN ARAÇ ÇAĞRILARI VE ÇIKTILARI:\n{cagri_cikti or '(araç çağrılmadı)'}\n\n"
            f"AGENT'IN CEVABI:\n{r['cevap']}\n\n"
            f"SİSTEM TALİMATI (agent'ın uyması gereken):\n{SISTEM_TALIMATI}")


def hakem_puanla(r):
    yanit = llm.istemci(HAKEM_MODEL).chat.completions.create(
        model=HAKEM_MODEL, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": hakem_talimati()},
                  {"role": "user", "content": hakem_mesaji(r)}])
    sonuc = json.loads(yanit.choices[0].message.content)
    gf, cf = FIYAT[HAKEM_MODEL]
    sonuc["hakem_maliyet"] = (yanit.usage.prompt_tokens * gf + yanit.usage.completion_tokens * cf) / 1e6
    return sonuc


def hakem_yapilanlar():
    return {(k["id"], k["model"], k["tekrar"], k["metin_modu"], k.get("deney", "v4")) for k in jsonl_oku(HAKEM_DOSYA)
            if k["hakem_model"] == HAKEM_MODEL and k["hakem_surum"] == HAKEM_SURUM}


def hepsini_puanla(df):
    """df'deki puanlanmamış cevapları hakeme verir (önbellek: 08_hakem.jsonl)."""
    bitti = hakem_yapilanlar()
    isler = [r for _, r in df.iterrows() if tuple(r[a] for a in ANAHTAR) not in bitti and pd.isna(r["hata"])]
    print(f"Hakem: {HAKEM_MODEL} · {HAKEM_SURUM} · puanlanacak: {len(isler)}")
    for r in tqdm(isler, desc="hakem"):
        try:
            h = hakem_puanla(r)
        except Exception as e:
            h = {"puan": None, "uydurma": None, "kural_ihlali": None, "gerekce": f"HAKEM HATASI: {e}", "hakem_maliyet": 0}
        kayit = {**{a: (int(r[a]) if a == "tekrar" else r[a]) for a in ANAHTAR},
                 "hakem_model": HAKEM_MODEL, "hakem_surum": HAKEM_SURUM, **h}
        jsonl_ekle(HAKEM_DOSYA, kayit)


def hakem_sonuclari():
    hk = pd.DataFrame(jsonl_oku(HAKEM_DOSYA))
    hk["deney"] = hk["deney"].fillna("v4")
    hk = hk[(hk["hakem_model"] == HAKEM_MODEL) & (hk["hakem_surum"] == HAKEM_SURUM)]
    return hk.drop_duplicates(ANAHTAR, keep="last")
