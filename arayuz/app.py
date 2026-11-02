"""Streamlit arayüzü: FastAPI servisine (src/api.py) bağlanan sohbet ekranı. Çalıştırma: streamlit run arayuz/app.py"""
import json
import os
import uuid

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


def iz_goster(c):
    with st.expander(f"Agent ne yaptı? · {len(c['araclar'])} araç · {c['tur']} tur · {c['sure']} sn · "
                     f"{c['girdi_token'] + c['cikti_token']:,} token".replace(",", ".")):
        if not c["araclar"]:
            st.write("Araç çağrılmadı.")
        for i, a in enumerate(c["araclar"], 1):
            durum = " ⚠️ hata" if a["hata"] else (" 🔁 tekrar engellendi" if a["tekrar"] else "")
            st.markdown(f"**{i}. `{a['ad']}`** · {a['sure']} sn{durum}")
            try:
                st.code(json.dumps(json.loads(a["argumanlar"]), ensure_ascii=False, indent=2), language="json")
            except json.JSONDecodeError:
                st.code(a["argumanlar"])
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
