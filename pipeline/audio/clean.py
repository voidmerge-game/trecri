"""تنظيف التعليق: قصّ الصمت (auto-editor إن توفر) + تطبيع الارتفاع إلى -16 LUFS."""
import argparse, json, os, shutil, subprocess

def trim(src, dst, threshold_db=-40):
    """قصّ الصمت: auto-editor أولاً، وعند أي فشل fallback إلى ffmpeg (لا فشل صامت ولا مخرج مزوّر)."""
    if shutil.which("auto-editor"):
        try:
            p = subprocess.run(["auto-editor", src, "--edit", f"audio:threshold={threshold_db}dB",
                                "--output", dst, "--no-open"],
                               capture_output=True, text=True, timeout=900)
            if p.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 1024:
                return {"trim": "auto-editor", "out": dst, "threshold_db": threshold_db}
            reason = (p.stdout or p.stderr or "")[-280:]
        except Exception as e:
            reason = str(e)[:200]
    else:
        reason = "auto-editor not installed"
    subprocess.run(["ffmpeg", "-y", "-i", src, "-af",
                    f"silenceremove=start_periods=1:start_threshold={threshold_db}dB:start_silence=0.2,"
                    f"areverse,silenceremove=start_periods=1:start_threshold={threshold_db}dB:start_silence=0.2,areverse",
                    dst], check=True, capture_output=True, timeout=900)
    return {"trim": "ffmpeg-silenceremove (fallback)", "out": dst, "auto_editor_reason": reason}

def normalise(src, dst, target=-16.0):
    subprocess.run(["ffmpeg", "-y", "-i", src, "-af",
                    f"loudnorm=I={target}:TP=-1.5:LRA=11", "-ar", "48000", dst],
                   check=True, capture_output=True)
    return {"normalise": "loudnorm", "target_lufs": target, "out": dst}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("--out", default="03_audio/narrator_clean.wav")
    a = ap.parse_args()
    t = trim(a.src, a.out.replace(".wav", "_trim.wav"))
    n = normalise(t["out"], a.out)
    print(json.dumps({"trim": t, "normalise": n}, indent=1))
