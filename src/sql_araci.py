"""SQL aracı (04_sql_araci'den taşındı): sql_calistir + oyun_bul."""
import re
import sqlite3
import time
from contextlib import closing

import pandas as pd
from rapidfuzz import fuzz, process

from src import ayarlar

SATIR_SINIRI = ayarlar.SATIR_SINIRI
ZAMAN_ASIMI_SN = ayarlar.ZAMAN_ASIMI_SN
METIN_MODU = ayarlar.METIN_MODU
KESME_UZUNLUGU = ayarlar.KESME_UZUNLUGU

METIN_SUTUNLARI = {("yorumlar", "metin"), ("oyunlar", "kisa_aciklama"), ("oyunlar", "oyun_hakkinda")}


def baglan():
    return sqlite3.connect(f"file:{ayarlar.DB_YOLU.as_posix()}?mode=ro", uri=True)


# ---------- sql_calistir ----------

def metin_bekcisi(islem, tablo, sutun, veritabani, kaynak):
    if islem == sqlite3.SQLITE_READ and (tablo, sutun) in METIN_SUTUNLARI:
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def hucre_kisalt(deger):
    if isinstance(deger, str) and len(deger) > KESME_UZUNLUGU:
        return deger[:KESME_UZUNLUGU] + f"...[kesildi, toplam {len(deger)} karakter]"
    return deger


def hata_mesaji(hata):
    if "interrupted" in str(hata):
        return (f"HATA: Sorgu {ZAMAN_ASIMI_SN} saniyeyi geçtiği için durduruldu. Daha dar bir sorgu yaz: "
                "app_id veya indeksli sütunlarla (dil, tarih) filtrele, bütün yorumlar tablosunu tarayan sorgulardan kaçın.")
    mesaj = f"HATA: {hata}"
    if "prohibited" in str(hata):
        mesaj += (" (Yorum metni ve oyun açıklamaları SQL aracında kapalı. İçerik için RAG aracını kullan; "
                  "sayı, oran ve filtre için bu sütunlar olmadan sorgu yaz.)")
    return mesaj


def sql_calistir(sorgu, sinir=None):
    sinir = sinir or SATIR_SINIRI
    sorgu = sorgu.strip().rstrip(";")
    baslangic = time.perf_counter()
    bitis = baslangic + ZAMAN_ASIMI_SN
    with closing(baglan()) as baglanti:
        if METIN_MODU == "gizle":
            baglanti.set_authorizer(metin_bekcisi)
        baglanti.set_progress_handler(lambda: 1 if time.perf_counter() > bitis else 0, 10_000)
        try:
            imlec = baglanti.execute(sorgu)
            if imlec.description is None:
                return "HATA: Sorgu tablo döndürmedi. Sadece SELECT sorgusu yaz."
            satirlar = imlec.fetchmany(sinir + 1)
            sutunlar = [s[0] for s in imlec.description]
            kesildi = len(satirlar) > sinir
            satirlar = satirlar[:sinir]
            if kesildi:
                toplam = baglanti.execute(f"SELECT COUNT(*) FROM ({sorgu})").fetchone()[0]
        except Exception as hata:
            return hata_mesaji(hata)
    sure = time.perf_counter() - baslangic

    df = pd.DataFrame(satirlar, columns=sutunlar)
    if METIN_MODU == "kes":
        df = df.map(hucre_kisalt)
    if kesildi:
        ozet = (f"DİKKAT: Sonuç {sinir} satırda kesildi. Sorgunun toplam sonucu {toplam:,} satır, "
                f"sadece ilk {sinir} tanesi gösteriliyor. Sayı lazımsa satırları kendin sayma, "
                f"COUNT(*) kullan. ({sure:.2f} sn)")
    else:
        ozet = f"{len(df)} satır, {sure:.2f} sn"
    return ozet + "\n" + df.to_csv(index=False)


# ---------- oyun_bul ----------

def ad_sadelestir(ad):
    return re.sub(r"[^\w]", "", ad.lower())


with closing(baglan()) as _b:
    oyun_adlari = pd.read_sql("SELECT app_id, ad, oy_sayisi, olumlu_oran FROM oyunlar", _b)
oyun_adlari["ad_sade"] = oyun_adlari["ad"].fillna("").map(ad_sadelestir)


def oyun_bul(isim, aday_sayisi=5):
    sonuclar = process.extract(ad_sadelestir(isim), oyun_adlari["ad_sade"], scorer=fuzz.WRatio, limit=20)
    adaylar = pd.DataFrame(
        [(oyun_adlari.loc[sira, "app_id"], oyun_adlari.loc[sira, "ad"], oyun_adlari.loc[sira, "oy_sayisi"],
          oyun_adlari.loc[sira, "olumlu_oran"], round(puan))
         for _, puan, sira in sonuclar],
        columns=["app_id", "ad", "oy_sayisi", "olumlu_oran", "benzerlik"],
    )
    return adaylar.sort_values(["benzerlik", "oy_sayisi"], ascending=False).head(aday_sayisi)


def oyun_bul_araci(isim):
    adaylar = oyun_bul(isim)
    return (
        f"'{isim}' için adı en çok benzeyen 5 oyun (benzerlik = ad benzerliği 0-100, kesin eşleşme anlamına gelmez; olumlu_oran = Steam oylarından genel puan, 0-1, boşsa oy yok):\n"
        f"{adaylar.to_csv(index=False)}"
        "Kural: Sorulan oyunu ad ve oy sayısına bakarak seç. Adaylardan hiçbiri sorulan oyun değilse "
        "(farklı bir oyun, Playtest, araç veya kart oyunu) oyunun veri setinde olmadığını söyle. "
        "Seçtiğin oyunu sonraki SQL sorgularında app_id ile kullan."
    )


# ---------- araç tanımları ----------

SQL_ARAC_ACIKLAMASI = """Steam oyun veritabanında (SQLite) salt okunur SQL sorgusu çalıştırır. Veri 2020-2024 arası Steam oyunlarını ve 2024 sonuna kadarki oyuncu yorumlarını kapsar.
Sonuç CSV olarak döner. En fazla 50 satır gösterilir; kesildiyse toplam satır sayısı yazılır. 10 saniyeyi geçen sorgu durdurulur.

NE ZAMAN KULLANILIR: sayı, oran, sıralama, filtreleme, sayım.
- Yorumların İÇERİĞİ (oyuncular ne diyor, şikâyetler, çökme var mı) için bu aracı değil RAG aracını kullan.
- Oyunu adıyla SQL'de arama. Önce oyun_bul aracıyla app_id'yi bul, sonra WHERE app_id = ... kullan.

TABLOLAR
oyunlar (64.948 oyun, birincil anahtar app_id)
- app_id, ad
- olumlu_oran: oyunun GENEL olumlu oy oranı, 0-1 arası (0.874 = %87,4). Oyunun puanı için TEK doğru kaynak. NULL = oy yok.
- oy_sayisi: toplam oy, popülerlik ölçüsü. oran_kaynagi: 'json', 'csv' veya NULL.
- yorum_sayisi: veritabanındaki yorum satırı sayısı. yorum_var: 1/0. yorum_kapsami: yorum_sayisi / oy_sayisi (0.06 = oyların %6'sının yorumu elimizde).
- olumlu_json, olumsuz_json, olumlu_csv, olumsuz_csv: ham sayılar. Oran için KULLANMA, olumlu_oran kullan.
- fiyat: verinin toplandığı günkü fiyat (indirimli olabilir). normal_fiyat: indirimsiz fiyat, fiyat sorularında bunu kullan. indirim_yuzde. Ücretsiz oyun: fiyat = 0.
- steam_cikis_tarihi ('YYYY-AA-GG'): Steam sayfasındaki tarih, oyunun ilk çıkışı OLMAYABİLİR. Oyunun ne zaman çıktığı için ilk_yorum_tarihi kullan. son_yorum_tarihi.
- sahip_alt, sahip_ust: tahmini sahip sayısı aralığı. peak_ccu: aynı anda en yüksek oyuncu sayısı. istatistik_eksik = 1 ise bu sütunlar ve oy bilgisi NULL.
- yorumcu_medyan_saat: yorum yazanların oynama süresi medyanı (saat). Oynama süresi sorularında bunu kullan. ortalama_sure_saat ve medyan_sure_saat sadece ~3.500 oyunda dolu. yorumcu_sure_sifir_orani.
- yas_siniri: sadece 422 oyunda dolu.
- tr_yorum_sayisi: Türkçe yorum sayısı. chroma_yorum_sayisi: RAG'da aranabilen yorum sayısı.
- Bayraklar (1/0): yetiskin (yetişkin içerik), iskelet (sayfası boş kayıt), dil_spam ve ses_spam (geliştirici neredeyse bütün dilleri işaretlemiş; dil bilgisine güvenme).
- kisa_aciklama, oyun_hakkinda: bu araçta KAPALI.

oyun_tur (app_id, tur): geliştiricinin seçtiği kaba tür. 'Action', 'Adventure', 'Casual', 'Indie', 'RPG', 'Simulation', 'Strategy', 'Sports', 'Racing', 'Massively Multiplayer', 'Early Access', 'Free To Play'. Korku türü yoktur.
oyun_etiket (app_id, etiket, oy, sira): oyuncuların verdiği etiketler, sira 1 = en çok oy alan. Tür benzeri sorularda (korku, roguelike vb.) etiket kullan, ör. 'Horror'. Yazılış: 'Singleplayer', 'Multiplayer' (tiresiz).
oyun_kategori (app_id, kategori): Steam özellikleri, iç içe: 'Multi-player' ⊃ 'PvP' ve 'Co-op' ⊃ 'Online PvP', 'Online Co-op', 'Shared/Split Screen PvP', 'Shared/Split Screen Co-op', 'LAN PvP', 'LAN Co-op'. Diğerleri: 'Single-player', 'Shared/Split Screen', 'Cross-Platform Multiplayer', 'MMO', 'VR Only', 'VR Supported', 'Full controller support', 'Steam Achievements'. İnternetten birlikte oynama = 'Online Co-op'.
oyun_dil (app_id, dil, ses_var): geliştiricinin beyan ettiği diller, İngilizce tam ad: 'English', 'Turkish', 'German', 'Simplified Chinese', 'Spanish - Spain', 'Portuguese - Brazil'. ses_var = 1 seslendirme var. Cevapta "geliştirici belirtmiş" de.

yorumlar (31,7 milyon yorum, birincil anahtar review_id)
- app_id, tarih ('YYYY-AA-GG'), olumlu (1/0), oynama_saat (yorum yazılırken), faydali_oy, erken_erisim (1/0), uzunluk (karakter).
- dil: tespit edilen dil KODU: 'en', 'zh', 'ru', 'es', 'pt', 'de', 'ko', 'tr', 'fr', 'ja' ... veya 'bilinmiyor'. (oyun_dil'deki 'Turkish' ile karıştırma.) dil_ham, dil_guven.
- resim, kopya (çöp ve kopya yorum, 1/0), chroma_uygun.
- metin: bu araçta KAPALI.
- İndeksli sütunlar: app_id, dil, tarih.

KURALLAR
1. Oyunun genel puanı = oyunlar.olumlu_oran. yorumlar.olumlu'dan AVG alma (yorumu eksik oyunlarda çok yanlış çıkar: The Sims 4 %87 yerine %56).
2. Alt grup oranı (dile, tarihe, oynama süresine göre) için yorumlar'dan AVG(olumlu) kullanılabilir. Cevapta "elimizdeki N yorumdan" de; yorum_kapsami 0.2'den küçükse bunun örneklem olduğunu belirt.
3. Öneri ve sıralama (saf olumlu_oran sıralaması az oylu, bilinmeyen oyunları öne çıkarır, YAPMA):
   a) "öner / iyi / beğenilen / popüler" → WHERE o.olumlu_oran >= 0.85 AND o.oy_sayisi >= 100 ... ORDER BY o.oy_sayisi DESC
   b) Sadece açıkça "en yüksek puanlı / en iyi puanlı" sorulursa → WHERE o.oy_sayisi >= 1000 ... ORDER BY o.olumlu_oran DESC. Eşiği cevapta söyle ("en az 1.000 oy alanlar arasında").
4. Sayı lazımsa COUNT(*) kullan, kesilmiş listeyi sayma. ORDER BY yazmazsan satırların sırası anlamsızdır.
5. Tarihi aralıkla filtrele: tarih >= '2024-01-01' AND tarih < '2025-01-01'. strftime kullanma (yavaş).
6. yorumlar sorgularını app_id, dil veya tarih ile daralt. Bütün yorumları tarayan sorgu zaman aşımına uğrar.
7. Kullanıcı açıkça istemedikçe yetiskin = 1 veya iskelet = 1 olan oyunları önerme.
8. Bir değerin yazılışından emin değilsen önce kontrol et, ör. SELECT DISTINCT etiket FROM oyun_etiket WHERE etiket LIKE '%rogue%'.
9. Sonuç 0 satırsa önce yazılışı kontrol et, sonra "veri yok" de.
10. Oranları kullanıcıya yüzde olarak söyle (0.952 → %95).
11. Etiket/tür/dil filtresini JOIN yerine EXISTS ile yaz (ör. EXISTS (SELECT 1 FROM oyun_etiket e WHERE e.app_id = o.app_id AND e.etiket = 'Horror')). JOIN + LIKE birden çok etiketle eşleşince aynı oyun birden fazla satırda çıkar.
"""
SQL_ARAC_TANIMLARI = [
    {"type": "function", "function": {
        "name": "sql_calistir",
        "description": SQL_ARAC_ACIKLAMASI,
        "parameters": {"type": "object", "properties": {
            "sorgu": {"type": "string", "description": "Çalıştırılacak tek bir SQLite SELECT sorgusu."}},
            "required": ["sorgu"]}}},
    {"type": "function", "function": {
        "name": "oyun_bul",
        "description": ("Oyun adını benzerlikle arar ve adı en çok benzeyen 5 oyunu (app_id, ad, oy_sayisi, olumlu_oran, benzerlik) döndürür. "
                        "Kullanıcı bir oyunun adını verdiğinde SQL'den ÖNCE bunu kullan, doğru oyunu seçip app_id'sini SQL'de kullan. "
                        "Adaylardan hiçbiri sorulan oyun değilse oyun veri setinde yoktur."),
        "parameters": {"type": "object", "properties": {
            "isim": {"type": "string", "description": "Kullanıcının yazdığı oyun adı, olduğu gibi (ör. 'sims 4')."}},
            "required": ["isim"]}}},
]

SQL_FONKSIYONLAR = {
    "sql_calistir": lambda sorgu: sql_calistir(sorgu),
    "oyun_bul": oyun_bul_araci,
}
