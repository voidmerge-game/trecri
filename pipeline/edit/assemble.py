"""التجميع بـ FFmpeg: zoompan لكل صورة + دمج + تعليق + موسيقى + LUT + ترجمة.

كل شيء قابل للتحقق. لا يُصدر أي حكم على الناتج — أرقام فقط.
"""
import argparse, json, os, shlex, subprocess

def sh(cmd, timeout=3600):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(shlex.quote(c) for c in cmd[:6])} ...\n{p.stderr[-1500:]}")
    return p

def zoompan_filter(idx, dur, fps, w, h, direction):
    frames = max(2, int(dur * fps))
    if direction == "in":   z = "min(1.0+0.0016*on,1.14)"
    elif direction == "out": z = "max(1.14-0.0016*on,1.0)"
    else:                    z = "1.06"
    x = f"iw/2-(iw/zoom/2)"; y = f"ih/2-(ih/zoom/2)"
    return (f"[{idx}:v]scale={w*2}:{h*2}:force_original_aspect_ratio=increase,"
            f"crop={w*2}:{h*2},zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={w}x{h}:fps={fps},"
            f"setsar=1[v{idx}]")

def build(timeline_path, out_path, audio=None, music=None, lut=None, srt=None, fps=24, w=1920, h=1080):
    tl = json.load(open(timeline_path, encoding="utf-8"))
    clips = [c for c in tl["clips"] if c.get("asset")]
    if not clips:
        raise SystemExit("لا توجد مقاطع بأصول — لم يُنتج ملف")
    inputs, filters, concat_in = [], [], []
    for i, c in enumerate(clips):
        inputs += ["-loop", "1", "-t", str(c["duration"]), "-i", c["asset"]]
        direction = ["in", "out", "none"][i % 3]
        filters.append(zoompan_filter(i, c["duration"], fps, w, h, direction))
        concat_in.append(f"[v{i}]")

    n = len(clips)
    fc = ";".join(filters) + ";" + "".join(concat_in) + f"concat=n={n}:v=1:a=0[vc]"
    post = []
    if lut:
        post.append(f"[vc]lut3d='{lut}'[vg]")
    else:
        post.append("[vc]null[vg]")
    if srt:
        post.append(f"[vg]subtitles='{srt}':force_style='FontName=DejaVu Serif,FontSize=22,PrimaryColour=&H00E6E1DA,Outline=1,Shadow=0'[vsub]")
    vout = "[vsub]" if srt else "[vg]"
    if post: fc += ";" + ";".join(post)

    cmd = ["ffmpeg", "-y"] + inputs
    aidx = None
    if audio:
        cmd += ["-i", audio]; aidx = n
    if music:
        cmd += ["-stream_loop", "-1", "-i", music]; midx = n + (1 if audio else 0)
    cmd += ["-filter_complex", fc, "-map", vout]
    if audio and music:
        fc2 = f"[{aidx}:a]volume=1.0[a1];[{midx}:a]volume=0.16[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=0,alimiter=limit=0.95[aout]"
        cmd[-1] = f"{vout};{fc2}"
        cmd += ["-map", "[aout]"]
    elif audio:
        cmd += ["-map", f"{aidx}:a"]
    elif music:
        cmd += ["-map", f"{midx}:a"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_path]
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    sh(cmd)
    return {"out": out_path, "clips": n, "fps": fps, "resolution": f"{w}x{h}"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", default="05_edit/timeline.json")
    ap.add_argument("--out", default="05_edit/assembly_v1.mp4")
    ap.add_argument("--audio"); ap.add_argument("--music"); ap.add_argument("--lut"); ap.add_argument("--srt")
    a = ap.parse_args()
    print(json.dumps(build(a.timeline, a.out, a.audio, a.music, a.lut, a.srt), indent=1))
