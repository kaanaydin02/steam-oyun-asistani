# Steam Oyun Analiz Asistanı

Steam oyun verisi ve oyuncu yorumları üzerinde Türkçe soru-cevap yapan LLM agent (SQL + RAG).

## Veri
"Steam Games Metadata and Player Reviews (2020–2024)", Mendeley Data, CC BY 4.0.
Repoda yoktur. İndirip şu yapıya koyun:
- data/raw/games.json
- data/raw/reviews/*.csv

## Kurulum
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
