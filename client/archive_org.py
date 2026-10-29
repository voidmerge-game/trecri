"""Archive.org — بحث + بيانات وصفية + ترخيص لكل عنصر. بلا مفتاح."""
from .base import get_json, urllib

def search(q, mediatype="movies", rows=10):
    params = {"q": f"{q} AND mediatype:{mediatype}", "fl[]": ["identifier", "title", "year", "licenseurl", "creator"],
              "rows": rows, "page": 1, "output": "json"}
    url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params, doseq=True)
    d = get_json(url)
    out = []
    for r in d.get("response", {}).get("docs", []):
        out.append({
            "identifier": r.get("identifier"),
            "title": r.get("title"),
            "year": r.get("year"),
            "creator": r.get("creator"),
            "license": r.get("licenseurl", ""),
            "file_url": f"https://archive.org/download/{r.get('identifier')}/",
            "details_url": f"https://archive.org/details/{r.get('identifier')}",
            "source": "archive.org",
        })
    return {"query": q, "total": d.get("response", {}).get("numFound"), "items": out, "endpoint": url}

def metadata(identifier):
    return get_json(f"https://archive.org/metadata/{identifier}")
