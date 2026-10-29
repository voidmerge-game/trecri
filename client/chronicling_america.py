"""Chronicling America (Library of Congress) — صحف تاريخية أمريكية. API عام بلا مفتاح.

ملاحظة تشغيلية: نقطة النهاية القديمة `chroniclingamerica.loc.gov/search/pages/results/?format=json`
توقفت عن الاستجابة، وقد نُقلت الخدمة إلى `loc.gov/collections/chronicling-america/`.
يستخدم هذا العميل النقطة الحالية، ويحتفظ بالقديمة كخيار احتياطي.
"""
from .base import get_json, urllib

NEW = "https://www.loc.gov/collections/chronicling-america/"
OLD = "https://chroniclingamerica.loc.gov/search/pages/results/"

def _norm_new(d):
    out = []
    for r in d.get("results", []):
        out.append({
            "title": r.get("title", ""),
            "date": r.get("date", ""),
            "newspaper": r.get("partof_title") or r.get("contributor", [""])[0] if isinstance(r.get("contributor"), list) else r.get("partof_title", ""),
            "state": r.get("location_state", [""])[0] if isinstance(r.get("location_state"), list) else r.get("location_state", ""),
            "page_url": r.get("id", ""),
            "ocr_url": (r.get("id", "") or "").rstrip("/") + "/ocr.txt",
            "image_url": (r.get("image_url") or [""])[0] if isinstance(r.get("image_url"), list) else r.get("image_url", ""),
            "image_full": iiif_full((r.get("image_url") or [""])[0] if isinstance(r.get("image_url"), list) else r.get("image_url", "")),
            "page_json": (r.get("url") or "").split("&q=")[0] + "&fo=json",
            "source": "loc.gov/collections/chronicling-america",
        })
    return out

def iiif_full(image_url, width=1600):
    """يحوّل رابط IIIF المصغّر إلى صورة كاملة العرض."""
    if not image_url: return ""
    base = image_url.split("/full/")[0]
    return f"{base}/full/{width},/0/default.jpg"

def search(text, date_from=None, date_to=None, state=None, rows=10, page=1):
    """نتائج موحّدة. يحاول النقطة الحالية أولاً ثم القديمة."""
    q = {"q": text, "fo": "json", "c": rows, "sp": page}
    if date_from and date_to: q["dates"] = f"{date_from}/{date_to}"
    elif date_from: q["dates"] = f"{date_from}/{date_from}"
    if state: q["fa"] = f"location_state:{state}"
    url = NEW + "?" + urllib.parse.urlencode(q)
    try:
        d = get_json(url, retries=1)
        items = _norm_new(d)
        if items:
            return {"query": q, "total": d.get("pagination", {}).get("of"), "items": items,
                    "endpoint": url, "api": "loc.gov"}
    except Exception:
        pass
    # fallback: القديمة
    q2 = {"andtext": text, "format": "json", "rows": rows, "page": page}
    if date_from: q2["date1"] = date_from
    if date_to: q2["date2"] = date_to
    url2 = OLD + "?" + urllib.parse.urlencode(q2)
    d = get_json(url2, retries=1)
    items = [{"title": i.get("title", ""), "date": i.get("date", ""),
              "newspaper": i.get("title_normal", ""), "state": i.get("state", ""),
              "page_url": i.get("id", ""),
              "ocr_url": (i.get("id", "") or "").rstrip("/") + "/ocr.txt",
              "image_url": (i.get("id", "") or "").rstrip("/") + ".jp2",
              "source": "chroniclingamerica.loc.gov"} for i in d.get("items", [])]
    return {"query": q2, "total": d.get("totalItems"), "items": items, "endpoint": url2, "api": "legacy"}
