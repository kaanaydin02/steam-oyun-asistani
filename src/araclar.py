"""Agent'ın gördüğü bütün araçlar tek yerde: tanımlar + tek çağırma kapısı."""
import json

from src.rag_araci import RAG_ARAC_TANIMLARI, RAG_FONKSIYONLAR, isinma
from src.sql_araci import SQL_ARAC_TANIMLARI, SQL_FONKSIYONLAR

ARAC_TANIMLARI = SQL_ARAC_TANIMLARI + RAG_ARAC_TANIMLARI
ARAC_FONKSIYONLARI = {**SQL_FONKSIYONLAR, **RAG_FONKSIYONLAR}


def arac_cagir(ad, argumanlar_json):
    if ad not in ARAC_FONKSIYONLARI:
        return f"HATA: '{ad}' diye bir araç yok. Kullanılabilir araçlar: {', '.join(ARAC_FONKSIYONLARI)}."
    try:
        argumanlar = json.loads(argumanlar_json) if argumanlar_json else {}
    except json.JSONDecodeError:
        return "HATA: Argümanlar geçerli JSON değil. Örnek: {\"sorgu\": \"SELECT ...\"}"
    for alan in ["app_id", "olumlu"]:
        if isinstance(argumanlar.get(alan), str) and argumanlar[alan].isdigit():
            argumanlar[alan] = int(argumanlar[alan])
    try:
        return ARAC_FONKSIYONLARI[ad](**argumanlar)
    except TypeError as e:
        return f"HATA: yanlış parametre ({e}). Şemadaki parametre adlarını kullan."
    except Exception as e:
        return f"HATA: araç çalışırken sorun çıktı ({type(e).__name__}: {e})."
