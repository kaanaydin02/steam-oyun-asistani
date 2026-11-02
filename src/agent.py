"""Elle yazılmış tool-calling agent (07). LangGraph sürümüyle aynı davranış hedeflenir."""
import json
import time

from src import llm
from src.araclar import ARAC_TANIMLARI, arac_cagir
from src.talimat import SISTEM_TALIMATI

VARSAYILAN_MODEL = "gpt-4.1-mini"
MAKS_TUR = 8


def calistir(soru, model=VARSAYILAN_MODEL, gecmis=None, maks_tur=MAKS_TUR, ayrintili=False):
    mesajlar = [{"role": "system", "content": SISTEM_TALIMATI},
                *(gecmis or []),
                {"role": "user", "content": soru}]
    iz = []
    girdi = cikti = 0
    t0 = time.perf_counter()
    tur_doldu = False

    for tur in range(1, maks_tur + 1):
        t = time.perf_counter()
        yanit = llm.sohbet(model, mesajlar, araclar=ARAC_TANIMLARI)
        m = yanit.choices[0].message
        girdi += yanit.usage.prompt_tokens
        cikti += yanit.usage.completion_tokens
        iz.append({"tur": tur, "tip": "llm", "sure": round(time.perf_counter() - t, 2),
                   "girdi": yanit.usage.prompt_tokens, "cikti": yanit.usage.completion_tokens})

        if not m.tool_calls:
            cevap = m.content
            break

        mesajlar.append(m.model_dump(exclude_none=True))
        for c in m.tool_calls:
            t = time.perf_counter()
            sonuc = arac_cagir(c.function.name, c.function.arguments)
            mesajlar.append({"role": "tool", "tool_call_id": c.id, "content": sonuc})
            iz.append({"tur": tur, "tip": "arac", "ad": c.function.name, "argumanlar": c.function.arguments,
                       "sure": round(time.perf_counter() - t, 2), "karakter": len(sonuc),
                       "hata": sonuc.startswith("HATA")})
            if ayrintili:
                print(f"[tur {tur}] {c.function.name}({c.function.arguments}) → {len(sonuc):,} kar.\n{sonuc[:300]}\n")
    else:
        tur_doldu = True
        yanit = llm.sohbet(model, mesajlar, araclar=ARAC_TANIMLARI, tool_choice="none")
        girdi += yanit.usage.prompt_tokens
        cikti += yanit.usage.completion_tokens
        cevap = yanit.choices[0].message.content

    mesajlar.append({"role": "assistant", "content": cevap})
    return {
        "soru": soru, "cevap": cevap, "model": model,
        "tur": tur, "tur_doldu": tur_doldu,
        "sure": round(time.perf_counter() - t0, 1),
        "girdi_token": girdi, "cikti_token": cikti,
        "araclar": [f"{a['ad']}({a['argumanlar']})" for a in iz if a["tip"] == "arac"],
        "iz": iz,
        "gecmis": mesajlar[1:],
    }


def iz_kaydet(sonuclar, dosya):
    with open(dosya, "a", encoding="utf-8") as f:
        for s in sonuclar:
            f.write(json.dumps({k: v for k, v in s.items() if k != "gecmis"}, ensure_ascii=False) + "\n")
