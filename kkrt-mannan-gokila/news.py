# ═══════════════════════════════════════════════
#  news.py — News store + AI sentiment (extend here)
# ═══════════════════════════════════════════════
news_store = []   # [{sym, s, head, impact, conf, sum}]


def add_news(sym: str, headline: str, sentiment: str = "up",
             impact: float = 5.0, conf: int = 70, summary: str = "") -> dict:
    """News item add pannum. sentiment: 'up' | 'dn' | 'nt'"""
    item = {
        "sym": sym, "s": sentiment, "head": headline,
        "impact": impact, "conf": conf, "sum": summary,
    }
    news_store.insert(0, item)
    del news_store[30:]
    return item


def get_news():
    return news_store
