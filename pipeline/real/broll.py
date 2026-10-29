"""مواد حقيقية من Archive.org / Commons / Pexels + ملف ترخيص لكل ملف + CREDITS."""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from client import archive_org, commons, pexels
from client.base import get_bytes, sha256

def fetch(query, outdir="04_visuals/broll", limit=4):
    os.makedirs(outdir, exist_ok=True)
    credits, items = [], []
    # Commons: صورة + ترخيص
    try:
        r = commons.search(query, limit=limit)
        for it in r["items"][:limit]:
            url = it.get("thumb") or it.get("url")
            if not url: continue
            data, _, _ = get_bytes(url)
            p = os.path.join(outdir, sha256(data)[:16] + ".jpg")
            open(p, "wb").write(data)
            rec = {"file": p, "source": "commons.wikimedia.org", "title": it["title"],
                   "license": it.get("license") or "UNKNOWN", "author": it.get("artist", ""), "url": url}
            items.append(rec)
            credits.append(f"- {os.path.basename(p)} — {it['title']} — {rec['license']} — {rec['author'][:80]} — {url}")
    except Exception as e:
        items.append({"source": "commons", "error": str(e)[:140]})
    # Archive.org: بيانات + ترخيص (بلا تنزيل ثقيل)
    try:
        r = archive_org.search(query, rows=limit)
        for it in r["items"][:limit]:
            items.append({"source": "archive.org", "identifier": it["identifier"], "title": it.get("title"),
                          "license": it.get("license") or "NO_LICENSE_FIELD",
                          "url": it["details_url"]})
    except Exception as e:
        items.append({"source": "archive.org", "error": str(e)[:140]})
    # Pexels: يسجّل MISSING_KEY إن غاب
    px = pexels.videos(query, per_page=2)
    items.append({"source": "pexels", "status": px.get("error", "OK"), "items": len(px.get("items", []))})

    with open(os.path.join(outdir, "CREDITS.md"), "a", encoding="utf-8") as f:
        f.write(f"\n## query: {query}\n" + "\n".join(credits) + "\n")
    with open(os.path.join(outdir, "sources.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    return {"downloaded": len(credits), "records": len(items)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("query"); ap.add_argument("--out", default="04_visuals/broll")
    ap.add_argument("--limit", type=int, default=4)
    a = ap.parse_args(); print(json.dumps(fetch(a.query, a.out, a.limit)))
