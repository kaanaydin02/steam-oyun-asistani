"""Streamlit arayüzü: FastAPI servisine (src/api.py) bağlanan sohbet ekranı. Çalıştırma: streamlit run arayuz/app.py"""
import io
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


def teknik_goster(a):
    """Geliştirici görünümü (11'deki sekmeler): RAG ayrıntısı / Çağrı / LLM'in gördüğü çıktı."""
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


# ---------------------------------------------------------------- son kullanıcı görünümü
# Teknik terim yok: "araç, mesafe, token" yerine "veritabanına baktı, yorum okudu, konuya ne kadar yakın".
SUTUN_ADI = {"ad": "Oyun", "olumlu_oran": "Olumlu oy", "oy_sayisi": "Oy sayısı", "yorum_sayisi": "Yorum sayısı",
             "normal_fiyat": "Normal fiyat ($)", "fiyat": "Güncel fiyat ($)", "indirim_yuzde": "İndirim (%)",
             "yorum_kapsami": "Yorumu elimizde olan oy oranı", "peak_ccu": "En yüksek anlık oyuncu",
             "yorumcu_medyan_saat": "Oynama süresi (saat, medyan)", "ilk_yorum_tarihi": "İlk yorum",
             "steam_cikis_tarihi": "Steam çıkış tarihi", "tr_yorum_sayisi": "Türkçe yorum", "tur": "Tür",
             "etiket": "Etiket", "yil": "Yıl", "adet": "Adet", "sayi": "Sayı"}


def benzerlik(m):
    """Mesafeyi kullanıcının anlayacağı kelimeye çevirir (sınırlar 06'da ölçüldü: 0,40 / 0,45)."""
    if m is None:
        return ""
    return "konuya çok yakın" if m <= ESLESME_SINIRLARI[0] else ("konuya yakın" if m <= ESLESME_SINIRLARI[1] else "konuya uzak")


def csv_oku(metin):
    try:
        return pd.read_csv(io.StringIO(metin))
    except Exception:
        return pd.DataFrame()


def sade_tablo(df):
    """SQL sonucunu okunur yapar: sütun adları Türkçe, oran yüzde, büyük sayılar noktalı, app_id gizli."""
    df = df.copy()
    for s in df.columns:
        if "oran" in s and pd.api.types.is_numeric_dtype(df[s]) and df[s].dropna().between(0, 1).all():
            df[s] = df[s].map(lambda x: "" if pd.isna(x) else f"%{x * 100:.1f}".replace(".", ","))
        elif pd.api.types.is_integer_dtype(df[s]) and s != "app_id":
            df[s] = df[s].map(lambda x: sayi(int(x)))
    if "app_id" in df and len(df.columns) > 1:
        df = df.drop(columns="app_id")
    yeni, kullanilan = [], set()
    for s in df.columns:                    # aynı Türkçe ada düşen iki sütun olursa ikincisi teknik adıyla kalır
        ad = SUTUN_ADI.get(s, s)
        yeni.append(ad if ad not in kullanilan else s)
        kullanilan.add(yeni[-1])
    df.columns = yeni
    return df


def yorum_karti(y, not_=None):
    """Tek yorum: alıntı + altında tavsiye / tarih / faydalı oy / konuya yakınlık."""
    metin = y["metin"].split(" [kesildi")[0].replace("\n", " ")
    metin = metin if len(metin) <= 220 else metin[:220].rsplit(" ", 1)[0] + "…"
    alt = ["👍 Tavsiye ediyor" if y["olumlu"] == 1 else "👎 Tavsiye etmiyor", str(y["tarih"])[:7]]
    if y.get("faydali_oy"):
        alt.append(f"{sayi(int(y['faydali_oy']))} kişi faydalı buldu")
    if not_:
        alt.append(not_)
    st.markdown(f"> {metin}\n>\n> <span style='font-size:.8rem;opacity:.7'>{' · '.join(alt)}</span>",
                unsafe_allow_html=True)


def adim_oyun_bul(a, arg):
    satirlar = a["cikti"].split("\n")[1:]
    df = csv_oku("\n".join(s for s in satirlar if s and not s.startswith("Kural:")))
    bulunan = f" ve **{df.iloc[0]['ad']}** oyununu buldu" if not df.empty else ""
    return "🔎", f"“{arg.get('isim', '')}” adını oyun listesinde aradı{bulunan}.", None


def adim_sql(a, arg):
    _, _, csv = a["cikti"].partition("\n")
    df = csv_oku(csv)

    def goster():
        if not df.empty:
            st.dataframe(sade_tablo(df.head(10)), hide_index=True)
            if len(df) > 10:
                st.caption(f"İlk 10 satır gösteriliyor, toplam {len(df)} satır.")
    return "📊", "Steam veritabanından sayıları çekti (puan, oy sayısı gibi kesin bilgiler buradan gelir).", goster


def adim_konu(d):
    y = d["yorumlar"]
    yakin = [v for v in y if v["mesafe"] <= ESLESME_SINIRLARI[1]]
    uzak = len(y) - len(yakin)
    nerede = "bu oyunun" if d.get("app_id") is not None else "bütün oyunların"
    cumle = (f"Oyuncu yorumlarında “{d['soru']}” konusunu aradı: {nerede} {sayi(d['taranan_parca'])} yorum parçası "
             f"arasından anlamca en yakın {len(y)} yorumu buldu.")
    if uzak:
        cumle += f" Bunlardan {uzak} tanesi konuya uzak olduğu için kanıt sayılmadı."

    def goster():
        for v in yakin or y[:2]:
            yorum_karti(v, benzerlik(v["mesafe"]))
    return "💬", cumle, goster


def adim_ozetle(d):
    cumle = (f"Oyunun {sayi(d['yorum_sayisi'])} oyuncu yorumu arasından, oyunu genel olarak değerlendiren ve "
             f"en çok “faydalı” oyu alan {len(d['olumlu'])} olumlu ve {len(d['olumsuz'])} olumsuz yorumu okudu.")

    def goster():
        sol, sag = st.columns(2)
        for kolon, grup, ad in [(sol, "olumlu", "👍 Beğenenler ne diyor?"), (sag, "olumsuz", "👎 Beğenmeyenler ne diyor?")]:
            with kolon:
                st.markdown(f"**{ad}**")
                for v in d[grup]:
                    yorum_karti(v)
                if not d[grup]:
                    st.caption("Bu grupta yorum yok.")
        st.caption("Agent bu yorumların hepsini okudu. Şaka, korsan ya da konu dışı olanları cevapta kullanmadı; "
                   "puanı yorumlardan değil Steam oylarından aldı.")
    return "💬", cumle, goster


def adim_hepsi(d):
    e = d["etiket_sayim"]
    cumle = (f"“{d['soru']}” konusuna değinen {sayi(d['aday'])} yorumu tek tek okuyup saydı: "
             f"**{e.get('evet', 0)} evet**, **{e.get('hayir', 0)} hayır**, {e.get('ilgisiz', 0)} konu dışı.")

    def goster():
        if d["yillar"]:
            yil = pd.DataFrame(d["yillar"]).set_index("yil")
            adlar = {"evet": "Evet diyen", "hayir": "Hayır diyen"}
            sutunlar = [c for c in adlar if c in yil]
            renk = {"evet": "#d1495b", "hayir": "#2e9e6a"}
            st.markdown("**Yıllara göre**")
            st.bar_chart(yil[sutunlar].rename(columns=adlar), color=[renk[c] for c in sutunlar], height=200)
        sol, sag = st.columns(2)
        for kolon, etiket, ad in [(sol, "evet", "Evet diyenlerden"), (sag, "hayir", "Hayır diyenlerden")]:
            with kolon:
                st.markdown(f"**{ad}**")
                for v in [v for v in d["yorumlar"] if v.get("etiket") == etiket][:2]:
                    yorum_karti(v)
        st.caption("Sayılar veri setindeki yorumlardan; Steam'deki bütün yorumlar değil.")
    return "🧮", cumle, goster


def adim_oyun_oner(d):
    cumle = (f"Oyun açıklamalarında “{d['istek']}” tarifine en çok benzeyen oyunları buldu, "
             f"az oy almış oyunları eledi ve {len(d['oyunlar'])} aday çıkardı.")

    def goster():
        df = pd.DataFrame(d["oyunlar"])
        if not df.empty:
            df["yakinlik"] = 1 - df["mesafe"]
            df["oy_sayisi"] = df["oy_sayisi"].map(lambda x: sayi(int(x)))
            st.dataframe(df[["ad", "oy_sayisi", "yakinlik"]], hide_index=True, column_config={
                "ad": "Oyun", "oy_sayisi": "Oy sayısı",
                "yakinlik": st.column_config.ProgressColumn("Tarife benzerlik", min_value=0.0, max_value=1.0, format=" ")})
    return "🎮", cumle, goster


def adim(a):
    """Bir araç çağrısını (simge, sade cümle, kanıtı gösteren fonksiyon) üçlüsüne çevirir."""
    if a["tekrar"]:
        return "🔁", "Aynı aramayı ikinci kez yapmak istedi; sonuç zaten elinde olduğu için atlandı.", None
    if a["hata"]:
        return "⚠️", "Bu adımda bir sorun çıktı, agent başka bir yoldan devam etti.", None
    try:
        arg = json.loads(a["argumanlar"] or "{}")
    except json.JSONDecodeError:
        arg = {}
    d = a.get("detay")
    if d:
        return {"konu": adim_konu, "ozetle": adim_ozetle, "hepsi": adim_hepsi, "oyun_oner": adim_oyun_oner}[d["mod"]](d)
    if a["ad"] == "oyun_bul":
        return adim_oyun_bul(a, arg)
    if a["ad"] == "sql_calistir":
        return adim_sql(a, arg)
    return "•", a["ad"], None


def kaynak_ozeti(c):
    """Başlık için: cevap hangi kaynaklara dayanıyor (veritabanı, kaç yorum, kaç oyun açıklaması)."""
    yorum, oyun, sql = 0, 0, False
    for a in c["araclar"]:
        d = {} if a["tekrar"] else (a.get("detay") or {})
        if a["ad"] == "sql_calistir" and not a["hata"]:
            sql = True
        if d.get("mod") == "konu":
            yorum += sum(v["mesafe"] <= ESLESME_SINIRLARI[1] for v in d["yorumlar"])
        elif d.get("mod") == "ozetle":
            yorum += len(d["olumlu"]) + len(d["olumsuz"])
        elif d.get("mod") == "hepsi":
            yorum += d["aday"]
        elif d.get("mod") == "oyun_oner":
            oyun += len(d["oyunlar"])
    parcalar = (["Steam veritabanı"] if sql else []) + ([f"{sayi(int(yorum))} oyuncu yorumu"] if yorum else []) \
        + ([f"{oyun} oyun açıklaması"] if oyun else [])
    return " + ".join(parcalar) or "araç kullanılmadı"


def iz_goster(c):
    teknik = st.session_state.get("teknik", False)
    with st.expander(f"🧭 Bu cevaba nasıl ulaştık? · {kaynak_ozeti(c)} · {c['sure']} sn"):
        for i, a in enumerate(c["araclar"], 1):
            simge, cumle, goster = adim(a)
            st.markdown(f"**{i}.** {simge} {cumle}")
            if goster:
                goster()
            if teknik:
                with st.container(border=True):
                    st.caption(f"🛠️ Teknik: `{a['ad']}` · {a['sure']} sn")
                    teknik_goster(a)
        st.markdown(f"**{len(c['araclar']) + 1}.** ✍️ Bu bilgileri birleştirip yukarıdaki cevabı yazdı.")
        ek = f" · {c['tur']} tur · {c['girdi_token'] + c['cikti_token']:,} token".replace(",", ".") if teknik else ""
        st.caption(f"Model: {c['model']}{ek}")


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
    st.toggle("🛠️ Teknik ayrıntılar", key="teknik",
              help="Açıkken her adımın altında SQL sorgusu, mesafeler ve LLM'e giden metin de görünür.")
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
                metin = (c["cevap"] or "_(boş cevap)_").replace("$", "\\$")
            except Exception as e:
                c, metin = None, f"❌ Hata: {e}"
        st.markdown(metin)
        if c:
            iz_goster(c)
    st.session_state.mesajlar.append({"rol": "assistant", "metin": metin, "cevap": c})
