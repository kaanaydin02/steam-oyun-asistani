"""Aynı agent'ın LangGraph sürümü: iki düğüm (llm, araclar) + koşullu kenar + hafıza (checkpointer)."""
import json
import operator
import time
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src import llm
from src.araclar import ARAC_TANIMLARI, arac_cagir
from src.talimat import SISTEM_TALIMATI

VARSAYILAN_MODEL = "gpt-4.1-mini"
MAKS_TUR = 8


class Durum(TypedDict):
    mesajlar: Annotated[list, operator.add]
    iz: Annotated[list, operator.add]
    model: str
    tur: int


def llm_dugumu(durum):
    tur = durum["tur"] + 1
    mesajlar = [{"role": "system", "content": SISTEM_TALIMATI}] + durum["mesajlar"]
    t = time.perf_counter()
    yanit = llm.sohbet(durum["model"], mesajlar, araclar=ARAC_TANIMLARI,
                       tool_choice="none" if tur > MAKS_TUR else None)
    m = yanit.choices[0].message
    kayit = {"tur": tur, "tip": "llm", "sure": round(time.perf_counter() - t, 2),
             "girdi": yanit.usage.prompt_tokens, "cikti": yanit.usage.completion_tokens}
    return {"mesajlar": [m.model_dump(exclude_none=True)], "iz": [kayit], "tur": tur}


TEKRAR_MESAJI = ("TEKRAR: Bu çağrıyı (aynı araç, aynı argümanlar) bu konuşmada zaten yaptın; sonucu yukarıdaki mesajlarda. "
                 "Aynı çağrıyı tekrarlama: farklı bir araç ya da argüman dene veya elindeki bilgiyle cevap ver.")


def cagri_anahtari(c):
    """Aynı çağrıyı tanımak için: araç adı + argümanların sıralı JSON hâli (boşluk/sıra farkı önemsiz)."""
    try:
        argumanlar = json.dumps(json.loads(c["function"]["arguments"] or "{}"), sort_keys=True, ensure_ascii=False)
    except json.JSONDecodeError:
        argumanlar = c["function"]["arguments"]
    return c["function"]["name"], argumanlar


def arac_dugumu(durum):
    son = durum["mesajlar"][-1]
    onceki = {cagri_anahtari(c) for m in durum["mesajlar"][:-1] for c in m.get("tool_calls") or []}
    yeni_mesajlar, kayitlar = [], []
    for c in son["tool_calls"]:
        t = time.perf_counter()
        anahtar = cagri_anahtari(c)
        tekrar = anahtar in onceki
        sonuc = TEKRAR_MESAJI if tekrar else arac_cagir(c["function"]["name"], c["function"]["arguments"])
        onceki.add(anahtar)
        yeni_mesajlar.append({"role": "tool", "tool_call_id": c["id"], "content": sonuc})
        kayitlar.append({"tur": durum["tur"], "tip": "arac", "ad": c["function"]["name"],
                         "argumanlar": c["function"]["arguments"], "sure": round(time.perf_counter() - t, 2),
                         "karakter": len(sonuc), "hata": sonuc.startswith("HATA"), "tekrar": tekrar})
    return {"mesajlar": yeni_mesajlar, "iz": kayitlar}


def sonraki(durum):
    return "araclar" if durum["mesajlar"][-1].get("tool_calls") else END


def graf_kur(hafiza=True):
    g = StateGraph(Durum)
    g.add_node("llm", llm_dugumu)
    g.add_node("araclar", arac_dugumu)
    g.add_edge(START, "llm")
    g.add_conditional_edges("llm", sonraki, ["araclar", END])
    g.add_edge("araclar", "llm")
    return g.compile(checkpointer=MemorySaver() if hafiza else None)


GRAF = graf_kur()


def calistir(soru, oturum="varsayilan", model=VARSAYILAN_MODEL):
    ayar = {"configurable": {"thread_id": oturum}}
    onceki = GRAF.get_state(ayar).values
    iz_bas = len(onceki.get("iz", []))
    t0 = time.perf_counter()
    son = GRAF.invoke({"mesajlar": [{"role": "user", "content": soru}], "iz": [], "model": model, "tur": 0}, ayar)
    iz = son["iz"][iz_bas:]
    return {
        "soru": soru, "cevap": son["mesajlar"][-1].get("content"), "model": model,
        "tur": son["tur"], "sure": round(time.perf_counter() - t0, 1),
        "girdi_token": sum(a.get("girdi", 0) for a in iz), "cikti_token": sum(a.get("cikti", 0) for a in iz),
        "araclar": [f"{a['ad']}({a['argumanlar']})" for a in iz if a["tip"] == "arac"],
        "iz": iz,
    }
