"""Wikimedia Commons — بحث صور/وسائط + ترخيص لكل ملف. بلا مفتاح."""
from .base import get_json, urllib

API = "https://commons.wikimedia.org/w/api.php"

def search(term, limit=10, filetype="bitmap"):
    params = {"action": "query", "format": "json", "generator": "search",
              "gsrsearch": f"filetype:{filetype} {term}", "gsrlimit": limit,
              "gsrnamespace": 6, "prop": "imageinfo",
              "iiprop": "url|extmetadata|size", "iiurlwidth": 1600}
    url = API + "?" + urllib.parse.urlencode(params)
    d = get_json(url)
    out = []
    for pid, p in (d.get("query", {}).get("pages", {}) or {}).items():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {}) or {}
        lic = (em.get("LicenseShortName", {}) or {}).get("value", "")
        out.append({
            "title": p.get("title"),
            "url": ii.get("url"),
            "thumb": ii.get("thumburl"),
            "width": ii.get("width"), "height": ii.get("height"),
            "license": lic,
            "artist": (em.get("Artist", {}) or {}).get("value", "")[:200],
            "source": "commons.wikimedia.org",
        })
    return {"query": term, "total": len(out), "items": out, "endpoint": url}
