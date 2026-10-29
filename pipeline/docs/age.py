"""تعتيق ورق: بقع، طيّات، تغيّر لون الحبر. مخرج يُعلَّم re-created دائماً."""
import argparse, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def age(src, out, seed=11, marks=True):
    random.seed(seed)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # صبغة ورق عتيق
    warm = Image.new("RGB", (w, h), (232, 220, 196))
    im = Image.blend(im, warm, 0.18)
    # بقع
    if marks:
        layer = Image.new("L", (w, h), 0); d = ImageDraw.Draw(layer)
        for _ in range(random.randint(6, 12)):
            x, y = random.randint(0, w), random.randint(0, h)
            r = random.randint(8, 44)
            d.ellipse([x-r, y-r, x+r, y+r], fill=random.randint(20, 55))
        layer = layer.filter(ImageFilter.GaussianBlur(9))
        stain = Image.new("RGB", (w, h), (170, 140, 96))
        im = Image.composite(stain, im, layer.point(lambda v: min(255, v*2)))
    # طيّات
    fold = Image.new("L", (w, h), 0); fd = ImageDraw.Draw(fold)
    for x in (w//3, 2*w//3):
        fd.line([(x, 0), (x, h)], fill=70, width=3)
    fd.line([(0, h//2), (w, h//2)], fill=55, width=3)
    fold = fold.filter(ImageFilter.GaussianBlur(3))
    dark = Image.new("RGB", (w, h), (120, 100, 70))
    im = Image.composite(dark, im, fold)
    # حبيبات
    noise = Image.effect_noise((w, h), 22).convert("L")
    im = ImageChops.overlay(im, Image.merge("RGB", (noise, noise, noise)))
    im.save(out, quality=92)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
    a = ap.parse_args(); print(age(a.src, a.out))
