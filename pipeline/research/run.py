"""مرحلة البحث: يجمع مصادر حقيقية، يؤرشفها، ويعمل OCR محلياً إن توفر tesseract.

لا يخترع نتائج. كل مخرج قابل للتحقق: ملف + هاش + سطر سجل.
الاستخدام:
  python -m pipeline.research.run --query "..." --from 1902 --to 1908 --rows 5
"""
import argparse, json, os, shutil, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from client import chronicling_america as ca, loc_api, archive_org, commons, freesound, pexels
from client.base import archive, ensure, get_bytes

OUT = "01_research"

def log_row(logfile, **kw):
    ensure(os.path.dirname(logfile))
    new = not os.path.exists(logfile)
    with open(logfile, "a", encoding="utf-8") as f:
        if new:
            f.write("unit,input,output,path,license,note\n")
        f.write(",".join(f'"{str(kw.get(k,""))}"' for k in
                ("unit","input","output","path","license","note")) + "\n")

def ocr(image_path, outdir):
    """OCR اختياري. إن غاب tesseract نُسجّل ذلك ولا نفشل."""
    if not shutil.which("tesseract"):
        return {"ocr": "SKIPPED", "reason": "tesseract not installed"}
    base = os.path.join(outdir, os.path.splitext(os.path.basename(image_path))[0])
    try:
        subprocess.run(["tesseract", image_path, base, "-l", "eng", "--psm", "3"],
                       check=True, capture_output=True, timeout=180)
        txt = base + ".txt"
        with open(txt, encoding="utf-8", errors="replace") as f:
            body = f.read()
        return {"ocr": "OK", "ocr_path": txt, "ocr_chars": len(body),
                "ocr_words": len(body.split())}
    except Exception as e:
        return {"ocr": "FAILED", "reason": str(e)[:120]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--from", dest="d1", default=None)
    ap.add_argument("--to", dest="d2", default=None)
    ap.add_argument("--rows", type=int, default=5)
    ap.add_argument("--state", default=None)
    a = ap.parse_args()

    ensure(OUT); ensure(os.path.join(OUT, "sources")); ensure(os.path.join(OUT, "pages"))
    index = {"query": a.query, "dates": [a.d1, a.d2], "collected_at":
             time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sources": {}, "archived": [], "skipped": []}

    # 1) Chronicling America — صور صحف + JSON الصفحة
    try:
        r = ca.search(a.query, a.d1, a.d2, a.state, rows=a.rows)
        index["sources"]["chronicling_america"] = {"api": r["api"], "total": r["total"], "items": len(r["items"])}
        for it in r["items"]:
            if it.get("image_full"):
                try:
                    data, hdrs, st = get_bytes(it["image_full"])
                    d = ensure(os.path.join(OUT, "pages"))
                    from client.base import sha256
                    h = sha256(data); p = os.path.join(d, h[:16] + ".jpg")
                    open(p, "wb").write(data)
                    rec = {"unit": "chronicling-america", "url": it["image_full"], "sha256": h,
                           "bytes": len(data), "path": p, "title": it["title"], "date": it["date"],
                           "license": "Public Domain (pre-1929 US periodical)"}
                    rec.update(ocr(p, d))
                    index["archived"].append(rec)
                    log_row(os.path.join(OUT, "log.csv"), unit="chronicling-america",
                            input=it["image_full"], output="page image + ocr",
                            path=rec["path"], license=rec["license"], note=rec.get("ocr", ""))
                except Exception as e:
                    index["skipped"].append({"url": it["image_full"], "reason": str(e)[:120]})
            else:
                index["skipped"].append({"url": it.get("page_url"), "reason": "no iiif image"})
    except Exception as e:
        index["sources"]["chronicling_america"] = {"error": str(e)[:160]}

    # 2) LoC عام
    try:
        r = loc_api.search(a.query, count=min(a.rows, 10))
        index["sources"]["loc_api"] = {"total": r["total"], "items": len(r["items"])}
        # نحتفظ بالبيانات فقط — تنزيل الصور في مرحلة لاحقة عند الحاجة
    except Exception as e:
        index["sources"]["loc_api"] = {"error": str(e)[:160]}

    # 3) Archive.org — بيانات وصفية + ترخيص
    try:
        r = archive_org.search(a.query, rows=min(a.rows, 10))
        index["sources"]["archive_org"] = {"total": r["total"], "items": len(r["items"]), "sample": r["items"][:3]}
    except Exception as e:
        index["sources"]["archive_org"] = {"error": str(e)[:160]}

    # 4) Commons — ترخيص لكل ملف
    try:
        r = commons.search(a.query, limit=min(a.rows, 10))
        index["sources"]["commons"] = {"total": r["total"], "items": len(r["items"]), "sample": r["items"][:3]}
    except Exception as e:
        index["sources"]["commons"] = {"error": str(e)[:160]}

    # 5) وحدات تحتاج مفتاحاً — تُسجَّل صراحةً كغير مُشغَّلة
    fs = freesound.search(a.query, page_size=3)
    px = pexels.videos(a.query, per_page=3)
    index["sources"]["freesound"] = {"status": fs.get("error", "OK"), "items": len(fs.get("items", []))}
    index["sources"]["pexels"] = {"status": px.get("error", "OK"), "items": len(px.get("items", []))}

    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)

    ok = len(index["archived"])
    print(f"archived={ok} skipped={len(index['skipped'])}")
    print(json.dumps({k: (v if isinstance(v, dict) else v) for k, v in index["sources"].items()},
                     ensure_ascii=False)[:600])
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
