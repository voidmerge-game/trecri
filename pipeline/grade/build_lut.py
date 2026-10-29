"""توليد LUT ثلاثي الأبعاد (.cube) بأسلوب داكن: teal/orange + رفع الظلال + هالة.

لا يعتمد على أي نموذج — رياضيات لونية فقط. يُطبَّق لاحقاً بـ ffmpeg lut3d.
الاستخدام: python -m pipeline.grade.build_lut out.cube --size 33
"""
import argparse

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))

def grade(r, g, b, strength=1.0, teal=0.06, warm=0.05, lift=0.012, gamma=1.06):
    # lift في الظلال
    r, g, b = r + lift, g + lift, b + lift
    # gamma
    r, g, b = r ** gamma, g ** gamma, b ** gamma
    # teal في الظلال / warm في الإضاءة
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    shadow = 1.0 - lum
    r += (-teal * shadow + warm * lum) * strength
    g += (teal * shadow * 0.6) * strength
    b += (teal * shadow) * strength
    # تباين حول 0.5
    r = (r - 0.5) * 1.08 + 0.5
    g = (g - 0.5) * 1.08 + 0.5
    b = (b - 0.5) * 1.06 + 0.5
    return clamp(r), clamp(g), clamp(b)

def write_cube(path, size=33, title="noir_dark_v1"):
    lines = [f'TITLE "{title}"', f"LUT_3D_SIZE {size}", "DOMAIN_MIN 0.0 0.0 0.0", "DOMAIN_MAX 1.0 1.0 1.0", ""]
    for bi in range(size):
        b = bi / (size - 1)
        for gi in range(size):
            g = gi / (size - 1)
            for ri in range(size):
                r = ri / (size - 1)
                R, G, B = grade(r, g, b)
                lines.append(f"{R:.6f} {G:.6f} {B:.6f}")
    open(path, "w").write("\n".join(lines) + "\n")
    return path

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--size", type=int, default=33)
    a = ap.parse_args(); write_cube(a.out, a.size); print("wrote", a.out)
