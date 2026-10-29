"""Library of Congress — عميل HTTP مباشر (بديل طبقة MCP). API عام بلا مفتاح."""
from .base import get_json, urllib

BASE = "https://www.loc.gov/"

def search(q, collection=None, fo="json", count=10):
    params = {"q": q, "fo": fo, "c": count}
    url = BASE + (f"collections/{collection}/" if collection else "search/") + "?" + urllib.parse.urlencode(params)
    d = get_json(url)
    out = []
    for r in d.get("results", [])[:count]:
        out.append({
            "title": r.get("title", ""),
            "date": r.get("date", ""),
            "url": r.get("id", "") or r.get("url", ""),
            "image_url": (r.get("image_url") or [""])[0] if isinstance(r.get("image_url"), list) else r.get("image_url"),
            "rights": r.get("rights", "") or r.get("rights_advisory", ""),
            "source": "loc.gov",
        })
    return {"query": q, "total": d.get("pagination", {}).get("of"), "items": out, "endpoint": url}
