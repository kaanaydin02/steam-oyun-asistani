"""LLM bağlantısı: model adını değiştirerek sağlayıcı değiştirilir (hepsi OpenAI uyumlu API)."""
import os

from openai import OpenAI

from src import ayarlar  # noqa: F401  (.env'i yükler)

SAGLAYICILAR = {
    "openai":   {"base_url": None,                                                       "anahtar": "OPENAI_API_KEY"},
    "gemini":   {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai/", "anahtar": "GEMINI_API_KEY"},
    "deepseek": {"base_url": "https://api.deepseek.com",                                 "anahtar": "DEEPSEEK_API_KEY"},
    "ollama":   {"base_url": f"{ayarlar.OLLAMA_URL}/v1",                                  "anahtar": None},
}

MODELLER = {
    "gpt-4.1-mini":     "openai",
    "gpt-6-luna":       "openai",
    "gemini-2.5-flash": "gemini",
    "deepseek-chat":    "deepseek",
    "qwen2.5:7b":       "ollama",
    "qwen2.5:14b":      "ollama",
    "gpt-6.1-terra":    "openai",
}

_istemciler = {}


def istemci(model):
    saglayici = MODELLER[model]
    if saglayici not in _istemciler:
        ayar = SAGLAYICILAR[saglayici]
        anahtar = os.getenv(ayar["anahtar"]) if ayar["anahtar"] else "ollama"
        if not anahtar:
            raise RuntimeError(f"{ayar['anahtar']} .env dosyasında yok ({model} için gerekli).")
        _istemciler[saglayici] = OpenAI(api_key=anahtar, base_url=ayar["base_url"], timeout=120)
    return _istemciler[saglayici]


# Modele özel ek API parametreleri (ör. düşünen modellerde araç çağırmak için düşünmeyi kapat)
MODEL_AYARLARI = {
    "gpt-6-luna": {"reasoning_effort": "none"},
}


def sohbet(model, mesajlar, araclar=None, temperature=0, tool_choice=None):
    ek = dict(MODEL_AYARLARI.get(model, {}))
    if tool_choice:
        ek["tool_choice"] = tool_choice
    return istemci(model).chat.completions.create(
        model=model, messages=mesajlar, tools=araclar, temperature=temperature, **ek)
