"""تنظيف التعليق: قصّ الصمت (auto-editor إن توفر) + تطبيع الارتفاع إلى -16 LUFS."""
import argparse, json, shutil, subprocess

def trim(src, dst):
    if shutil.which("auto-editor"):
        subprocess.run(["auto-editor", src, "--edit", "audio:threshold=-40dB",
                        "--output", dst, "--no-open"], check=True, capture_output=True, timeout=1200)
        return {"trim": "auto-editor", "out": dst}
    subprocess.run(["ffmpeg", "-y", "-i", src, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.25,"
                    "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.25,areverse",
                    dst], check=True, capture_output=True)
    return {"trim": "ffmpeg-silenceremove (fallback)", "out": dst}

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
