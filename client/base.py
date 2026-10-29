"""عقد موحّد لكل عميل: get_json / get_bytes / archive. لا مفاتيح في الكود."""
import json, hashlib, os, time, urllib.request, urllib.parse

UA = "tr-research/1.0 (+research pipeline)"
ROOT = os.environ.get("OUT_DIR", "01_research")

def _req(url, headers=None, timeout=45):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers: h.update(headers)
    return urllib.request.Request(url, headers=h)

def get_json(url, headers=None, retries=2, timeout=45):
    last = None
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(_req(url, headers, timeout), timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"GET failed {url}: {last}")

def get_bytes(url, headers=None, timeout=120):
    with urllib.request.urlopen(_req(url, headers, timeout), timeout=timeout) as r:
        return r.read(), dict(r.headers), r.status

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def ensure(p):
    os.makedirs(p, exist_ok=True)
    return p

def archive(url, subdir="sources", headers=None, ext=".bin"):
    """ينزّل المصدر ويحفظه + سطر بيان بالهاش. يُعيد dict."""
    data, hdrs, status = get_bytes(url, headers)
    d = ensure(os.path.join(ROOT, subdir))
    h = sha256(data)
    path = os.path.join(d, h[:16] + ext)
    if not os.path.exists(path):
        with open(path, "wb") as f: f.write(data)
    return {"url": url, "sha256": h, "bytes": len(data), "status": status,
            "content_type": hdrs.get("Content-Type", ""), "path": path,
            "archived_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
