"""بناء timeline.json من shotlist + أصول بصرية. لا يقرر إبداعياً — يجمع فقط.

المدخل: 02_script/shotlist.json + 04_visuals/**  (صور/خرائط/وثائق)
المخرج: 05_edit/timeline.json  (قائمة مقاطع بترتيب المشاهد)
"""
import argparse, glob, json, os, re

PRIORITY = {"page": ["pages/", "docs/"], "map": ["maps/"], "portrait": ["docs/", "pages/"],
            "wide": ["broll/", "pages/"], "medium": ["pages/", "broll/"], "detail": ["docs/", "pages/"]}

SRC_RE = re.compile(r"\s*\[SRC:[^\]]*\]")

def text_card(text, out, w=1920, h=1080):
    """بطاقة نصية داكنة تُستخدم عندما لا يوجد أصل بصري. ليست صورة أرشيفية."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (w, h), (16, 18, 21))
    d = ImageDraw.Draw(im)
    try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 46)
    except Exception: font = ImageFont.load_default()
    clean = SRC_RE.sub("", text or "").strip()
    words, lines, cur = clean.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) > w - 320: lines.append(cur); cur = wd
        else: cur = t
    if cur: lines.append(cur)
    y = h//2 - (len(lines) * 30)
    for ln in lines[:7]:
        d.text((160, y), ln, font=font, fill=(226, 222, 214)); y += 62
    d.text((160, h - 90), "SOURCE CARD", font=font, fill=(90, 96, 104))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    im.save(out, quality=92)
    return out

def pool(root):
    files = {}
    for d in ("pages", "docs", "maps", "broll", "evidence"):
        files[d] = sorted(glob.glob(os.path.join(root, d, "**", "*.*"), recursive=True))
    return files

def build(shotlist_path, visuals_root, out_path, fps=24):
    sl = json.load(open(shotlist_path, encoding="utf-8"))
    files = pool(visuals_root)
    clips, used = [], set()
    for sh in sl["shots"]:
        pick = None
        for d in PRIORITY.get(sh["type"], ["pages"]):
            for f in files.get(d.rstrip("/"), []):
                if f not in used and f.lower().endswith((".jpg", ".jpeg", ".png")):
                    pick = f; break
            if pick: break
        if pick:
            used.add(pick)
        else:
            pick = text_card(sh["text"], os.path.join(visuals_root, "cards", sh["shot_id"] + ".jpg"))
        clips.append({"shot_id": sh["shot_id"], "scene": sh["scene"], "type": sh["type"],
                      "asset": pick, "duration": round(sh["duration_hint_s"], 2),
                      "text": sh["text"], "sources": sh["sources"],
                      "motion": "zoompan", "disclosure": None})
    tl = {"fps": fps, "resolution": [1920, 1080], "clip_count": len(clips),
          "with_asset": sum(1 for c in clips if c["asset"]), "clips": clips}
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    json.dump(tl, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return tl

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shotlist", default="02_script/shotlist.json")
    ap.add_argument("--visuals", default="04_visuals")
    ap.add_argument("--out", default="05_edit/timeline.json")
    a = ap.parse_args()
    t = build(a.shotlist, a.visuals, a.out)
    print(f"clips={t['clip_count']} with_asset={t['with_asset']} -> {a.out}")
