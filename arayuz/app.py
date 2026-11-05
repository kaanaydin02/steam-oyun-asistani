"""Streamlit arayüzü: FastAPI servisine (src/api.py) bağlanan sohbet ekranı. Çalıştırma: streamlit run arayuz/app.py"""
import json
import os
import uuid

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
ORNEK_SORULAR = [
    "Baldur's Gate 3'ün puanı ve oy sayısı nedir?",
    "The Sims 4'ü oyuncular seviyor mu?",
    "Elden Ring'i eleştirenler neden şikâyet ediyor?",
    "Arkadaşlarla oynanacak online co-op korku oyunu öner.",
    "En çok Türkçe yorum alan oyunlar hangileri?",
]

st.set_page_config(page_title="Steam Oyun Asistanı", page_icon="🎮", layout="centered")


@st.cache_data(ttl=60)
def modelleri_getir():
    r = requests.get(f"{API_URL}/modeller", timeout=5)
    r.raise_for_status()
    return r.json()


def yeni_sohbet():
    st.session_state.oturum = uuid.uuid4().hex
    st.session_state.mesajlar = []


def sor(soru, model):
    r = requests.post(f"{API_URL}/sor", json={"soru": soru, "oturum": st.session_state.oturum, "model": model},
                      timeout=300)
    if r.status_code != 200:
        raise RuntimeError(r.json().get("detail", r.text))
    return r.json()


# ---------------------------------------------------------------- RAG ayrıntısı
ACIKLAMA = """
**Embedding:** Her yorum, anlamını temsil eden 1024 sayılık bir vektöre çevrildi (qwen3-embedding:4b). Aynı şeyi anlatan yorumların vektörleri birbirine yakın düşer, dilleri farklı olsa bile.

**Mesafe:** Soru ile yorum vektörü arasındaki uzaklık (1 − kosinüs benzerliği). 0 = aynı anlam. Bu projede ölçtüğümüz aralıklar: **≤ 0,40 güçlü**, 0,40–0,45 orta, **> 0,45 zayıf** (agent'a "kanıt sayma" denir).

**Yakınlık çubuğu:** 1 − mesafe. Çubuk uzunsa yorum soruya anlamca yakın.

**Faydalı oy:** Steam'de yorumu "faydalı" bulan kişi sayısı. Şaka yorumlar da çok oy alabildiği için tek başına kullanılmıyor.
"""
MOD_ADI = {"konu": "Konu araması", "ozetle": "Genel özet", "hepsi": "Sayım (bütün ilgili yorumlar)"}
ESLESME_SINIRLARI = (0.40, 0.45)


def eslesme(m):
    if m is None:
        return ""
    return "🟢 güçlü" if m <= ESLESME_SINIRLARI[0] else ("🟡 orta" if m <= ESLESME_SINIRLARI[1] else "🔴 zayıf")


def sayi(x):
    return f"{x:,}".replace(",", ".") if isinstance(x, int) else str(x)


def akis(adimlar):
    """Adım zinciri: [(sayı, açıklama), ...] → kutular ve oklar."""
    kutular = "".join(
        f'<div style="border:1px solid rgba(128,128,128,.35);border-radius:8px;padding:6px 10px;min-width:0">'
        f'<div style="font-size:1.25rem;font-weight:700;line-height:1.2">{s}</div>'
        f'<div style="font-size:.78rem;opacity:.75;line-height:1.25">{a}</div></div>'
        + ('<div style="align-self:center;opacity:.5">➜</div>' if i < len(adimlar) - 1 else "")
        for i, (s, a) in enumerate(adimlar))
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 10px">{kutular}</div>',
                unsafe_allow_html=True)


YORUM_SUTUNLARI = {
    "eslesme": st.column_config.TextColumn("eşleşme"),
    "yakinlik": st.column_config.ProgressColumn("yakınlık", min_value=0.0, max_value=1.0, format="%.2f",
                                                help="1 − mesafe; uzun çubuk = anlamca yakın"),
    "mesafe": st.column_config.NumberColumn("mesafe", format="%.3f"),
    "faydali_oy": st.column_config.NumberColumn("faydalı oy"),
    "durum": st.column_config.TextColumn("tavsiye"),
    "metin": st.column_config.TextColumn("yorum (ilk 300 karakter)", width="large"),
}


def yorum_tablosu(yorumlar, sutunlar=("eslesme", "yakinlik", "mesafe", "faydali_oy", "durum", "dil", "tarih", "metin")):
    df = pd.DataFrame(yorumlar)
    if df.empty:
        st.caption("Yorum yok.")
        return
    df["durum"] = df["olumlu"].map({1: "👍", 0: "👎"})
    df["eslesme"] = df["mesafe"].map(eslesme)
    df["yakinlik"] = 1 - df["mesafe"]
    st.dataframe(df[[s for s in sutunlar if s in df]], hide_index=True, column_config=YORUM_SUTUNLARI)


def rag_goster(d):
    """yorum_ara / oyun_oner ayrıntısı: arama adım adım nasıl yapıldı + LLM'e hangi yorumlar gitti."""
    with st.popover("ℹ️ Bu tablo ne demek?"):
        st.markdown(ACIKLAMA)

    if d["mod"] == "oyun_oner":
        st.markdown(f"**Oyun önerisi** · istek: _{d['istek']}_")
        akis([("23.218", "oyun açıklaması Chroma'da"), ("200", "isteğe en yakın oyun"),
              (f"oy ≥ {d['min_oy']}", "az oylu" + (" ve yetişkin" if d["yetiskin_haric"] else "") + " oyunlar atıldı"),
              ("sırala", f"skor = mesafe − {d['w']} × log10(oy)"), (len(d["oyunlar"]), "oyun LLM'e gitti")])
        df = pd.DataFrame(d["oyunlar"])
        if not df.empty:
            df["yakinlik"] = 1 - df["mesafe"]
            st.dataframe(df[["ad", "oy_sayisi", "yakinlik", "mesafe", "skor", "app_id"]], hide_index=True, column_config={
                "yakinlik": YORUM_SUTUNLARI["yakinlik"], "mesafe": st.column_config.NumberColumn(format="%.3f"),
                "skor": st.column_config.NumberColumn(format="%.3f", help="küçük = daha uygun")})
        return

    filtreler = [f"{k}={d[k]}" for k in ["olumlu", "dil"] if isinstance(d.get(k), (int, str))]
    st.markdown(f"**{MOD_ADI[d['mod']]}** · mod `{d['mod']}` · oyun `{d.get('app_id')}`"
                + (f" · filtre `{', '.join(filtreler)}`" if filtreler else ""))

    if d["mod"] == "konu":
        y = d["yorumlar"]
        guclu = sum(v["mesafe"] <= ESLESME_SINIRLARI[1] for v in y)
        akis([(sayi(d["taranan_parca"]), d["arama"]),
              ("vektör", f"“{d['soru']}” embedding'e çevrildi"),
              (len(y), "en yakın yorum (aynı yorumun parçaları tekilleştirildi)"),
              (f"{guclu} / {len(y) - guclu}", f"güçlü-orta / zayıf (> {d['zayif_esik']})"),
              ("LLM", "zayıfları kanıt saymadan okudu")])
        yorum_tablosu(y)

    elif d["mod"] == "ozetle":
        akis([(d["yorum_sayisi"], "oyunun örneklemdeki yorumu"),
              (f"{d['olumlu_toplam']} / {d['olumsuz_toplam']}", "olumlu / olumsuz grup"),
              (f"{d['olumlu_aday']} / {d['olumsuz_aday']}", "1. eleme: genel değerlendirmeye en yakın yarısı (en fazla 40)"),
              (f"{len(d['olumlu'])} / {len(d['olumsuz'])}", "2. eleme: en çok faydalı oy alanlar"),
              ("LLM", "puanı SQL'den, nedeni bu yorumlardan aldı")])
        st.caption(f"Karşılaştırılan cümle: “{d['genel_sorgu']}”. Örneklemdeki olumlu/olumsuz oranı genel puan değildir.")
        for grup, ad in [("olumlu", "👍 Olumlu yorumlar"), ("olumsuz", "👎 Olumsuz yorumlar")]:
            kesim = d.get(f"{grup}_kesim")
            st.markdown(f"**{ad}** · faydalı oya göre"
                        + (f" · 1. elemeden geçme sınırı: mesafe ≤ {kesim:.3f} {eslesme(kesim)}" if kesim is not None else ""))
            if kesim is not None and kesim > ESLESME_SINIRLARI[1]:
                st.caption(f"⚠️ Bu grupta en yakın adaylar bile genel değerlendirme cümlesine uzak (> {ESLESME_SINIRLARI[1]}). "
                           "Yorumlar kısa ya da oyunu değerlendirmiyor; şaka veya konu dışı yorum sızabilir, LLM kurallarla eler.")
            yorum_tablosu(d[grup], ("faydali_oy", "eslesme", "yakinlik", "mesafe", "dil", "tarih", "metin"))

    elif d["mod"] == "hepsi":
        e = d["etiket_sayim"]
        akis([(d["yorum_sayisi"], "oyunun örneklemdeki yorumu"),
              (d["aday"], f"soruya mesafesi ≤ {d['esik']} olan aday"),
              (f"{e.get('evet', 0)} / {e.get('hayir', 0)} / {e.get('ilgisiz', 0)}",
               f"evet / hayır / ilgisiz ({d['etiket_modeli']} her yorumu tek tek okudu)"),
              ("pandas", "sayım ve yıllara bölme"), ("LLM", "sayıları ve örnekleri okudu")])
        st.caption(f"Soru: “{d['soru']}” · evet = yorum soruya evet diyor, hayır = konuya değinip hayır diyor. "
                   "Sayılar örneklemden; eşik bazı ilgili yorumları kaçırabilir, oranı 'en az' diye okumak gerekir.")
        if d["yillar"]:
            yil = pd.DataFrame(d["yillar"]).set_index("yil")
            renkler = {"evet": "#d1495b", "hayir": "#2e9e6a", "ilgisiz": "#9aa5b1"}
            sutunlar = [c for c in ["evet", "hayir", "ilgisiz"] if c in yil]
            sol, sag = st.columns([3, 2])
            with sol:
                st.markdown("**Yıllara göre etiketler**")
                st.bar_chart(yil[sutunlar], color=[renkler[c] for c in sutunlar], height=220)
            with sag:
                st.dataframe(yil[sutunlar])
        st.markdown("**Bütün adaylar ve etiketleri** (mesafeye göre)")
        df = pd.DataFrame(d["yorumlar"])
        if not df.empty:
            df["etiket"] = df["etiket"].map({"evet": "🔴 evet", "hayir": "🟢 hayır", "ilgisiz": "⚪ ilgisiz"}).fillna(df["etiket"])
        yorum_tablosu(df.to_dict("records"), ("etiket", "gerekce", "eslesme", "yakinlik", "tarih", "durum", "metin"))


def iz_goster(c):
    rag_sayisi = sum(1 for a in c["araclar"] if a.get("detay"))
    with st.expander(f"Agent ne yaptı? · {len(c['araclar'])} araç ({rag_sayisi} RAG) · {c['tur']} tur · {c['sure']} sn · "
                     f"{c['girdi_token'] + c['cikti_token']:,} token".replace(",", ".")):
        if not c["araclar"]:
            st.write("Araç çağrılmadı.")
        for i, a in enumerate(c["araclar"], 1):
            durum = " ⚠️ hata" if a["hata"] else (" 🔁 tekrar engellendi" if a["tekrar"] else "")
            with st.container(border=True):
                st.markdown(f"**{i}. `{a['ad']}`** · {a['sure']} sn{durum}")
                try:
                    argumanlar = json.loads(a["argumanlar"] or "{}")
                except json.JSONDecodeError:
                    argumanlar = None
                sekmeler = (["🔎 RAG ayrıntısı"] if a.get("detay") else []) + ["Çağrı", "LLM'in gördüğü çıktı"]
                tablar = st.tabs(sekmeler)
                if a.get("detay"):
                    with tablar[0]:
                        rag_goster(a["detay"])
                with tablar[-2]:
                    if a["ad"] == "sql_calistir" and argumanlar:
                        st.code(argumanlar.get("sorgu", ""), language="sql")
                    elif argumanlar is not None:
                        st.code(json.dumps(argumanlar, ensure_ascii=False, indent=2), language="json")
                    else:
                        st.code(a["argumanlar"])
                with tablar[-1]:
                    st.code(a.get("cikti") or "(boş)", language="text")
        st.caption(f"Model: {c['model']}")


# ---------------------------------------------------------------- durum
if "oturum" not in st.session_state:
    yeni_sohbet()

# ---------------------------------------------------------------- kenar çubuğu
with st.sidebar:
    st.header("🎮 Steam Oyun Asistanı")
    try:
        bilgi = modelleri_getir()
        model = st.selectbox("Model", bilgi["modeller"], index=bilgi["modeller"].index(bilgi["varsayilan"]),
                             help="09'daki karşılaştırmada en iyi sonuç gpt-6-luna (varsayılan).")
    except requests.RequestException:
        st.error(f"API'ye ulaşılamadı: {API_URL}\n\n`uvicorn src.api:app --port 8000` çalışıyor mu?")
        st.stop()
    st.button("🗑️ Yeni sohbet", on_click=yeni_sohbet, width="stretch")
    st.subheader("Örnek sorular")
    for s in ORNEK_SORULAR:
        if st.button(s, width="stretch"):
            st.session_state.bekleyen = s
    st.caption("Veri: Steam Games Metadata and Player Reviews (2020–2024), Mendeley, CC BY 4.0. "
               "Puanlar Steam oylarından (SQL), yorum özetleri oyuncu yorumlarından (RAG).")

# ---------------------------------------------------------------- sohbet
st.title("Steam oyunları hakkında sor")
for m in st.session_state.mesajlar:
    with st.chat_message(m["rol"]):
        st.markdown(m["metin"])
        if m.get("cevap"):
            iz_goster(m["cevap"])

soru = st.chat_input("Örn: Cyberpunk 2077 çıkışından bu yana düzeldi mi?") or st.session_state.pop("bekleyen", None)
if soru:
    st.session_state.mesajlar.append({"rol": "user", "metin": soru})
    with st.chat_message("user"):
        st.markdown(soru)
    with st.chat_message("assistant"):
        with st.spinner(f"{model} düşünüyor, araçları kullanıyor..."):
            try:
                c = sor(soru, model)
                metin = c["cevap"] or "_(boş cevap)_"
            except Exception as e:
                c, metin = None, f"❌ Hata: {e}"
        st.markdown(metin)
        if c:
            iz_goster(c)
    st.session_state.mesajlar.append({"rol": "assistant", "metin": metin, "cevap": c})
