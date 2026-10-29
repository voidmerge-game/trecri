"""رسالة بخط اليد بالإنجليزية على ورق — نص فقط، بلا استنساخ خط شخص حقيقي."""
import argparse, random
from PIL import Image, ImageDraw, ImageFont

FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]

def render(text, out, w=1400, h=1000, seed=7):
    random.seed(seed)
    im = Image.new("RGB", (w, h), (238, 232, 216))
    d = ImageDraw.Draw(im)
    try: font = ImageFont.truetype(FONTS[0], 34)
    except Exception: font = ImageFont.load_default()
    d.rectangle([60, 60, w-60, h-60], outline=(200, 190, 170), width=2)
    y = 130
    for para in text.split("\n"):
        words, line = para.split(), ""
        for wd in words:
            trial = (line + " " + wd).strip()
            if d.textlength(trial, font=font) > w - 220:
                d.text((110 + random.randint(-1,1), y), line, font=font, fill=(38, 34, 30)); y += 52; line = wd
            else:
                line = trial
        if line:
            d.text((110 + random.randint(-1,1), y), line, font=font, fill=(38, 34, 30)); y += 52
        y += 14
        if y > h - 140: break
    im.save(out, quality=92)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("text"); ap.add_argument("out")
    a = ap.parse_args(); print(render(a.text, a.out))
