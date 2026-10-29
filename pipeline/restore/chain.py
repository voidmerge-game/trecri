"""سلسلة الترميم بالترتيب الإلزامي: GFPGAN → تكبير → إزالة عيوب → تلوين.

كل خطوة تُفحص فعلياً. ما لا يعمل يُسجَّل SKIPPED مع السبب — لا نتيجة مزوّرة.
يعمل على CPU. لا GPU مطلوب.
"""
import argparse, importlib.util, json, os, shutil, subprocess

MAX_SIDE = 1280

def shrink(src, out_dir, max_side=MAX_SIDE):
    """تصغير قبل المعالجة: صفحات الصحف 1600px+ تُبطئ النماذج على CPU بشكل قاتل."""
    from PIL import Image
    im = Image.open(src)
    if max(im.size) <= max_side:
        return src, False
    r = max_side / max(im.size)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    p = os.path.join(out_dir, "0_small.png")
    im.save(p)
    return p, True

def has(mod):
    return importlib.util.find_spec(mod) is not None

def has_bin(name):
    return shutil.which(name) is not None

def step_face(src, dst):
    """GFPGAN: ترميم الوجوه — يُشغَّل فقط إن كانت الحزمة قابلة للاستيراد."""
    if not has("gfpgan"):
        return {"step": "gfpgan", "role": "face restoration", "status": "SKIPPED",
                "reason": "python package 'gfpgan' not importable"}
    code = (
        "import sys,cv2\n"
        "from gfpgan import GFPGANer\n"          # noqa
        "r=GFPGANer(model_path=None,upscale=1,arch='clean',channel_multiplier=2,bg_upsampler=None)\n"
        f"_,_,out=r.enhance(sys.argv[1],has_aligned=False,only_center_face=False,paste_back=True)\n"
        f"cv2.imwrite(sys.argv[2],out)\n"
    )
    p = subprocess.run(["python3", "-c", code, src, dst], capture_output=True, text=True, timeout=420)
    if p.returncode != 0 or not os.path.exists(dst):
        return {"step": "gfpgan", "role": "face restoration", "status": "FAILED",
                "reason": (p.stderr or "")[-300:]}
    return {"step": "gfpgan", "role": "face restoration", "status": "OK", "output": dst}

def step_upscale(src, dst, scale=2):
    """Real-ESRGAN إن توفر؛ وإلا تكبير LANCZOS معلَّم صراحةً كبديل."""
    if has("realesrgan") and has("basicsr"):
        code = (
            "import sys,cv2\n"
            "from basicsr.archs.rrdbnet_arch import RRDBNet\n"
            "from realesrgan import RealESRGANer\n"
            "m=RRDBNet(num_in_ch=3,num_out_ch=3,num_feat=64,num_block=23,num_grow_ch=32,scale=4)\n"
            "u=RealESRGANer(scale=4,model_path=sys.argv[3],model=m,tile=0,tile_pad=10,pre_pad=0,half=False)\n"
            "img=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED)\n"
            "o,_=u.enhance(img,outscale=float(sys.argv[4]))\n"
            "cv2.imwrite(sys.argv[2],o)\n"
        )
        weights = "RealESRGAN_x4plus.pth"
        if os.path.exists(weights):
            p = subprocess.run(["python3", "-c", code, src, dst, weights, str(scale)],
                               capture_output=True, text=True, timeout=420)
            if p.returncode == 0 and os.path.exists(dst):
                return {"step": "upscale", "role": "super resolution", "status": "OK",
                        "engine": "Real-ESRGAN", "output": dst}
        reason = "weights or run failed"
    else:
        reason = "realesrgan/basicsr not importable"
    from PIL import Image
    im = Image.open(src)
    im.resize((im.width * scale, im.height * scale), Image.LANCZOS).save(dst)
    return {"step": "upscale", "role": "super resolution", "status": "OK",
            "engine": "Pillow LANCZOS (documented fallback, not Real-ESRGAN)",
            "reason_for_fallback": reason, "output": dst}

def step_inpaint(src, dst_dir):
    """إزالة عيوب: قناع تلقائي من البكسلات شديدة السواد (خدوش/بقع)."""
    if not has_bin("iopaint"):
        return {"step": "iopaint", "role": "defect removal", "status": "SKIPPED",
                "reason": "binary 'iopaint' not available"}
    from PIL import Image
    import numpy as np
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype("uint8")
    mask = (a.mean(axis=2) < 40).astype("uint8") * 255
    if mask.sum() == 0:
        return {"step": "iopaint", "role": "defect removal", "status": "SKIPPED",
                "reason": "auto-mask found no defects to remove"}
    mp = dst_dir + "/mask.png"
    Image.fromarray(mask).save(mp)
    p = subprocess.run(["iopaint", "run", "--model=lama", "--device=cpu",
                        f"--image={src}", f"--mask={mp}", f"--output={dst_dir}"],
                       capture_output=True, text=True, timeout=420)
    cand = [os.path.join(dst_dir, f) for f in os.listdir(dst_dir) if f.lower().endswith((".png", ".jpg"))]
    if p.returncode != 0 or len(cand) < 2:
        return {"step": "iopaint", "role": "defect removal", "status": "FAILED",
                "reason": (p.stderr or "")[-300:]}
    return {"step": "iopaint", "role": "defect removal", "status": "OK",
            "output": sorted(cand)[-1], "mask": mp}

def step_colourise(src, dst):
    """تلوين إعادة بناء — يُعلَّم إلزاماً Colourised reconstruction."""
    from PIL import Image, ImageOps
    im = Image.open(src).convert("L")
    ImageOps.colorize(im, black="#12100e", white="#e8dcc0").save(dst)
    lum = Image.open(dst).convert("L").resize((1, 1)).getpixel((0, 0))
    return {"step": "colourise", "role": "colour reconstruction", "status": "OK",
            "disclosure": "Colourised reconstruction", "output": dst}

def run_chain(src, outdir, colourise=True, max_side=MAX_SIDE):
    os.makedirs(outdir, exist_ok=True)
    small, was_shrunk = shrink(src, outdir, max_side)
    log, cur = [], small
    if was_shrunk:
        log.append({"step": "preprocess", "role": "downscale for CPU", "status": "OK",
                    "note": f"downscaled to max side {max_side}", "output": small})
    r = step_face(cur, os.path.join(outdir, "1_face.png"))
    log.append(r)
    if r["status"] == "OK": cur = r["output"]
    r = step_upscale(cur, os.path.join(outdir, "2_upscale.png"))
    log.append(r)
    if r["status"] == "OK": cur = r["output"]
    d = os.path.join(outdir, "3_inpaint"); os.makedirs(d, exist_ok=True)
    r = step_inpaint(cur, d)
    log.append(r)
    if r["status"] == "OK": cur = r["output"]
    if colourise:
        r = step_colourise(cur, os.path.join(outdir, "4_colourised.png"))
        log.append(r)
        if r["status"] == "OK": cur = r["output"]
    log.append({"step": "final", "output": cur})
    json.dump(log, open(os.path.join(outdir, "restore_log.json"), "w"), ensure_ascii=False, indent=1)
    return log

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("outdir")
    ap.add_argument("--no-colour", action="store_true")
    ap.add_argument("--max-side", type=int, default=MAX_SIDE)
    a = ap.parse_args()
    print(json.dumps(run_chain(a.src, a.outdir, not a.no_colour, a.max_side), ensure_ascii=False, indent=1))
