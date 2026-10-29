"""قصاصة صحيفة مصنّعة — تُعلَّم re-created على الصورة نفسها (إفصاح إلزامي)."""
import argparse
from PIL import Image, ImageDraw, ImageFont

def build(headline, body, out, w=900, h=1150, date="19—"):
    im = Image.new("RGB", (w, h), (240, 235, 222)); d = ImageDraw.Draw(im)
    def F(sz):
        try: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", sz)
        except Exception: return ImageFont.load_default()
    try: fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 20)
    except Exception: fb = ImageFont.load_default()
    d.rectangle([0, 0, w-1, h-1], outline=(190, 182, 165), width=3)
    d.text((50, 46), "THE EVENING RECORD", font=F(30), fill=(30, 30, 30))
    d.line([(50, 92), (w-50, 92)], fill=(40, 40, 40), width=2)
    d.text((w-140, 50), date, font=fb, fill=(60, 60, 60))
    y = 120
    for line in headline.upper().split("\n"):
        d.text((50, y), line, font=F(38), fill=(15, 15, 15)); y += 50
    d.line([(50, y+10), (w-50, y+10)], fill=(80, 80, 80), width=1); y += 34
    words = body.split(); line = ""
    for wd in words:
        t = (line + " " + wd).strip()
        if d.textlength(t, font=fb) > w - 110:
            d.text((50, y), line, font=fb, fill=(25, 25, 25)); y += 28; line = wd
        else: line = t
    if line: d.text((50, y), line, font=fb, fill=(25, 25, 25))
    # إفصاح إلزامي
    d.rectangle([0, h-46, w, h], fill=(22, 22, 22))
    d.text((22, h-36), "RE-CREATED DOCUMENT — not an original artefact", font=fb, fill=(235, 232, 226))
    im.save(out, quality=93)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--headline", required=True); ap.add_argument("--body", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); print(build(a.headline, a.body, a.out))
