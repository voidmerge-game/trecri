"""استخراج متوسط إحصائي من صورة مرجعية → معاملات LUT.

لا ينسخ إطلالة فيلم محمي؛ يستخرج **متوسطات لونية** ويستخدمها كمرجع أسلوبي عام.
الاستخدام: python -m pipeline.grade.look_extract ref.jpg --out look.json
"""
import argparse, json
from PIL import Image

def stats(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((256, 256))
    px = list(im.getdata()); n = len(px)
    mr = sum(p[0] for p in px) / n / 255
    mg = sum(p[1] for p in px) / n / 255
    mb = sum(p[2] for p in px) / n / 255
    lum = 0.2126 * mr + 0.7152 * mg + 0.0722 * mb
    sat = (max(mr, mg, mb) - min(mr, mg, mb))
    return {"mean_r": round(mr, 4), "mean_g": round(mg, 4), "mean_b": round(mb, 4),
            "mean_luma": round(lum, 4), "spread": round(sat, 4),
            "suggestion": {"teal": round(max(0, mb - mr) * 1.2, 4),
                           "warm": round(max(0, mr - mb) * 1.2, 4),
                           "lift": round(0.5 - lum, 4) if lum < 0.5 else 0.0}}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("img"); ap.add_argument("--out", default="look.json")
    a = ap.parse_args(); d = stats(a.img)
    json.dump(d, open(a.out, "w"), indent=1); print(json.dumps(d))
