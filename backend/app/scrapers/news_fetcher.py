import datetime as dt
import requests
from bs4 import BeautifulSoup
import feedparser

def fetch_rss(url: str, source: str, limit: int = 10):
    out = []
    feed = feedparser.parse(url)
    for e in feed.entries[:limit]:
        ts = getattr(e, "published_parsed", None) or getattr(e, "updated_parsed", None)
        when = dt.datetime(*ts[:6]) if ts else dt.datetime.utcnow()
        out.append({
            "title": getattr(e, "title", "(sin título)"),
            "source": source,
            "url": getattr(e, "link", url),
            "published_at": when,
            "summary": getattr(e, "summary", "")[:600]
        })
    return out

def fetch_sat_boletines(limit:int=8):
    url = "https://www.gob.mx/sat/es/archivo/articulos?idiom=es"
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("ul.archived-news li")[:limit]
    out=[]
    for it in items:
        a = it.select_one("a")
        if not a: continue
        title = a.get_text(strip=True)
        href = a.get("href") or url
        if href.startswith("/"):
            href = "https://www.gob.mx" + href
        out.append({"title": title, "source": "SAT", "url": href,
                    "published_at": dt.datetime.utcnow(), "summary": ""})
    return out

def fetch_all_sources():
    items = []
    try:
        items += fetch_rss("https://www.banxico.org.mx/rss/comunicados.rss", "Banxico", 8)
    except Exception:
        pass
    try:
        items += fetch_sat_boletines(8)
    except Exception:
        pass
    seen=set(); out=[]
    for it in items:
        if it["url"] in seen: continue
        seen.add(it["url"]); out.append(it)
    return out