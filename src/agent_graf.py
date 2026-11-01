"""Aynı agent'ın LangGraph sürümü: iki düğüm (llm, araclar) + koşullu kenar + hafıza (checkpointer)."""
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
    if tur > MAKS_TUR:
        yanit = llm.istemci(durum["model"]).chat.completions.create(
            model=durum["model"], messages=mesajlar, tools=ARAC_TANIMLARI, tool_choice="none", temperature=0)
    else:
        yanit = llm.sohbet(durum["model"], mesajlar, araclar=ARAC_TANIMLARI)
    m = yanit.choices[0].message
    kayit = {"tur": tur, "tip": "llm", "sure": round(time.perf_counter() - t, 2),
             "girdi": yanit.usage.prompt_tokens, "cikti": yanit.usage.completion_tokens}
    return {"mesajlar": [m.model_dump(exclude_none=True)], "iz": [kayit], "tur": tur}


def arac_dugumu(durum):
    son = durum["mesajlar"][-1]
    yeni_mesajlar, kayitlar = [], []
    for c in son["tool_calls"]:
        t = time.perf_counter()
        sonuc = arac_cagir(c["function"]["name"], c["function"]["arguments"])
        yeni_mesajlar.append({"role": "tool", "tool_call_id": c["id"], "content": sonuc})
        kayitlar.append({"tur": durum["tur"], "tip": "arac", "ad": c["function"]["name"],
                         "argumanlar": c["function"]["arguments"], "sure": round(time.perf_counter() - t, 2),
                         "karakter": len(sonuc), "hata": sonuc.startswith("HATA")})
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
