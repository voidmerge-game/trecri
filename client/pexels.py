"""Pexels — يحتاج مفتاحاً في PEXELS_KEY. يرجع بسبب واضح إن غاب."""
import os
from .base import get_json, urllib

def videos(q, per_page=10, orientation="landscape"):
    key = os.environ.get("PEXELS_KEY")
    if not key:
        return {"error": "MISSING_KEY", "env": "PEXELS_KEY", "items": [], "total": 0}
    url = f"https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": q, "per_page": per_page, "orientation": orientation})
    d = get_json(url, headers={"Authorization": key})
    out = [{"id": v["id"], "url": v.get("url"), "duration": v.get("duration"),
            "license": "Pexels License (attribution not required, do not resell)",
            "files": [f.get("link") for f in v.get("video_files", [])][:2],
            "source": "pexels.com"} for v in d.get("videos", [])]
    return {"query": q, "total": d.get("total_results"), "items": out, "endpoint": "api.pexels.com"}
