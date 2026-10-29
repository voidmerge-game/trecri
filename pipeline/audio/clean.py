"""تنظيف التعليق: قصّ الصمت + تطبيع الارتفاع.

قاعدة النزاهة: كل خطوة تُتحقَّق بـ ffprobe. إن أنتجت خطوة ملفاً تالفاً (0 ثانية أو
حجم صغير جداً) يُرفض ويُستخدم البديل، ويُسجَّل السبب. لا ملف تالف يمرّ بصمت.
"""
import argparse, json, os, shutil, subprocess

MIN_BYTES = 2048
MIN_SECONDS = 0.4


def probe(path):
    if not os.path.exists(path):
        return {"exists": False}
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=channels,sample_rate,codec_name",
                        "-of", "json", path], capture_output=True, text=True)
    if p.returncode != 0:
        return {"exists": True, "valid": False, "stderr": p.stderr[-200:]}
    d = json.loads(p.stdout or "{}")
    dur = float(d.get("format", {}).get("duration") or 0)
    size = int(d.get("format", {}).get("size") or 0)
    st = (d.get("streams") or [{}])[0]
    return {"exists": True, "valid": dur >= MIN_SECONDS and size >= MIN_BYTES,
            "duration_s": round(dur, 3), "bytes": size,
            "channels": st.get("channels"), "sample_rate": st.get("sample_rate")}


def trim(src, dst, threshold_db=-40):
    """قصّ الصمت. auto-editor أولاً، ثم ffmpeg، والتحقق في كل مرة."""
    reasons = []
    if shutil.which("auto-editor"):
        try:
            p = subprocess.run(["auto-editor", src, "--edit", f"audio:threshold={threshold_db}dB",
                                "--output", dst, "--no-open"],
                               capture_output=True, text=True, timeout=900)
            info = probe(dst)
            if p.returncode == 0 and info.get("valid"):
                return {"trim": "auto-editor", "out": dst, "probe": info}
            reasons.append(f"auto-editor: rc={p.returncode} probe={info}")
        except Exception as e:
            reasons.append(f"auto-editor: {e}")
    else:
        reasons.append("auto-editor not installed")

    # fallback: قصّ الصمت في الطرفين عبر silencedetect + atrim (أدق من silenceremove على ملفات concat)
    try:
        det = subprocess.run(["ffmpeg", "-i", src, "-af",
                              f"silencedetect=noise={threshold_db}dB:d=0.2", "-f", "null", "-"],
                             capture_output=True, text=True, timeout=600).stderr
        starts = [float(l.split("silence_start:")[1].split()[0]) for l in det.splitlines() if "silence_start:" in l]
        ends = [float(l.split("silence_end:")[1].split()[0]) for l in det.splitlines() if "silence_end:" in l]
        total = probe(src).get("duration_s", 0.0)
        cut_from = ends[0] if starts and ends and starts[0] < 0.05 else 0.0
        cut_to = starts[-1] if starts and total and starts[-1] > total - 0.3 else total
        if cut_to - cut_from < MIN_SECONDS:
            cut_from, cut_to = 0.0, total
        subprocess.run(["ffmpeg", "-y", "-i", src, "-af",
                        f"atrim=start={cut_from:.3f}:end={cut_to:.3f},asetpts=PTS-STARTPTS",
                        dst], check=True, capture_output=True, timeout=600)
        info = probe(dst)
        if info.get("valid"):
            return {"trim": "ffmpeg-silencedetect+atrim", "out": dst, "probe": info,
                    "cut": [round(cut_from, 3), round(cut_to, 3)], "reasons": reasons}
        reasons.append(f"ffmpeg-trim invalid: {info}")
    except Exception as e:
        reasons.append(f"ffmpeg-trim: {e}")

    # آخر حل: نسخ المصدر كما هو (بلا قصّ) — معلَّم صراحةً
    shutil.copyfile(src, dst)
    return {"trim": "NO-TRIM (source copied)", "out": dst, "probe": probe(dst), "reasons": reasons}


def normalise(src, dst, target=-16.0):
    """تطبيع الارتفاع. يتحقق من المخرج، ويقع على نسخة مباشرة عند الفشل."""
    try:
        subprocess.run(["ffmpeg", "-y", "-i", src, "-af",
                        f"loudnorm=I={target}:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", dst],
                       check=True, capture_output=True, timeout=900)
        info = probe(dst)
        if info.get("valid"):
            return {"normalise": "loudnorm", "target_lufs": target, "out": dst, "probe": info}
    except Exception as e:
        err = str(e)[:200]
    else:
        err = f"invalid output: {probe(dst)}"
    subprocess.run(["ffmpeg", "-y", "-i", src, "-ar", "48000", "-ac", "2", dst],
                   check=True, capture_output=True, timeout=600)
    return {"normalise": "resample only (loudnorm failed)", "out": dst,
            "probe": probe(dst), "reason": err}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--out", default="03_audio/narrator_clean.wav")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    tmp = a.out.replace(".wav", "_trim.wav")
    t = trim(a.src, tmp)
    n = normalise(t["out"], a.out)
    rep = {"source": probe(a.src), "trim": t, "normalise": n, "final": probe(a.out)}
    json.dump(rep, open(a.out.replace(".wav", "_report.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    raise SystemExit(0 if rep["final"].get("valid") else 1)
