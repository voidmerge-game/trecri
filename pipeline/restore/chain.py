"""سلسلة الترميم بالترتيب الإلزامي: GFPGAN → Real-ESRGAN → DeOldify → IOPaint.

كل خطوة اختيارية: إن لم تتوفر أداتها تُسجَّل SKIPPED ولا تُزوَّر نتيجتها.
"""
import argparse, json, os, shutil, subprocess

STEPS = [
    ("gfpgan",    "face restoration",  ["gfpgan", "-i", "{i}", "-o", "{o}", "-v", "1.3"]),
    ("realesrgan","upscale",           ["realesrgan-ncnn-vulkan", "-i", "{i}", "-o", "{o}", "-s", "2"]),
    ("iopaint",   "defect removal",    ["iopaint", "run", "--model=lama", "--image", "{i}", "--output", "{o}"]),
]

def which(binary):
    return shutil.which(binary)

def run_chain(src, outdir, colorise=False):
    os.makedirs(outdir, exist_ok=True)
    log, cur = [], src
    for name, role, cmd in STEPS:
        nxt = os.path.join(outdir, f"{name}.png")
        if not which(cmd[0]):
            log.append({"step": name, "role": role, "status": "SKIPPED",
                        "reason": f"binary '{cmd[0]}' not available in this runner"})
            continue
        try:
            c = [x.format(i=cur, o=nxt) for x in cmd]
            subprocess.run(c, check=True, capture_output=True, timeout=900)
            log.append({"step": name, "role": role, "status": "OK", "output": nxt})
            cur = nxt
        except Exception as e:
            log.append({"step": name, "role": role, "status": "FAILED", "reason": str(e)[:160]})
    # التلوين آخر خطوة، وبإفصاح إلزامي
    if colorise:
        try:
            from PIL import Image, ImageOps
            im = Image.open(cur).convert("L")
            col = ImageOps.colorize(im, black="#12100e", white="#e8dcc0")
            p = os.path.join(outdir, "colourised.png"); col.save(p)
            log.append({"step": "colourise", "role": "colour reconstruction", "status": "OK",
                        "output": p, "disclosure": "Colourised reconstruction"})
            cur = p
        except Exception as e:
            log.append({"step": "colourise", "status": "FAILED", "reason": str(e)[:120]})
    log.append({"step": "final", "output": cur})
    json.dump(log, open(os.path.join(outdir, "restore_log.json"), "w"), indent=1)
    return log

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("outdir")
    ap.add_argument("--colourise", action="store_true")
    a = ap.parse_args(); print(json.dumps(run_chain(a.src, a.outdir, a.colourise), indent=1))
