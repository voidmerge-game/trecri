"""Freesound — يحتاج مفتاح API في FREESOUND_KEY. يرجع بسبب واضح إن غاب."""
import os
from .base import get_json, urllib

API = "https://freesound.org/apiv2/search/text/"

def search(q, duration_max=None, license_filter="Creative Commons 0", page_size=10):
    key = os.environ.get("FREESOUND_KEY")
    if not key:
        return {"error": "MISSING_KEY", "env": "FREESOUND_KEY", "items": [], "total": 0}
    params = {"query": q, "fields": "id,name,license,previews,duration,filesize",
              "page_size": page_size, "filter": f'license:"{license_filter}"'}
    if duration_max: params["filter"] += f" duration:[0 TO {duration_max}]"
    url = API + "?" + urllib.parse.urlencode(params)
    d = get_json(url, headers={"Authorization": f"Token {key}"})
    out = [{"id": r["id"], "name": r["name"], "license": r["license"],
            "duration": r.get("duration"), "preview": (r.get("previews") or {}).get("preview-hq-mp3"),
            "source": "freesound.org"} for r in d.get("results", [])]
    return {"query": q, "total": d.get("count"), "items": out, "endpoint": "freesound.org/apiv2"}
