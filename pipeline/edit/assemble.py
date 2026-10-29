"""التجميع بـ FFmpeg: zoompan لكل صورة + دمج + تعليق + موسيقى + LUT + ترجمة.

كل شيء قابل للتحقق. لا يُصدر أي حكم على الناتج — أرقام فقط.
"""
import argparse, json, os, shlex, subprocess

def sh(cmd, timeout=900):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(shlex.quote(c) for c in cmd[:6])} ...\n{p.stderr[-1500:]}")
    return p

def zoompan_filter(idx, dur, fps, w, h, direction):
    """إطار واحد ثابت ← N إطاراً متحركاً.

    تحذير تشغيلي مهم: لا تستخدم -loop 1 مع zoompan. مع d>1 يُنتج zoompan
    d إطاراً *لكل إطار إدخال*، فيتضاعف العدد بلا نهاية ويعلّق التجميع.
    الحل: إطار واحد فقط + d = عدد الإطارات المطلوبة، والتكبير عبر متغيّر zoom.
    """
    frames = max(2, int(round(dur * fps)))
    if direction == "in":
        z = "min(zoom+0.0012,1.14)"
    elif direction == "out":
        z = "if(eq(on,1),1.14,max(zoom-0.0012,1.0))"
    else:
        z = "1.04"
    x = "iw/2-(iw/zoom/2)"; y = "ih/2-(ih/zoom/2)"
    return (f"[{idx}:v]scale={w*2}:{h*2}:force_original_aspect_ratio=increase,"
            f"crop={w*2}:{h*2},zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={w}x{h}:fps={fps},"
            f"trim=duration={dur},setpts=PTS-STARTPTS,setsar=1[v{idx}]")

def audio_valid(path):
    """ffprobe: هل الملف الصوتي صالح فعلاً؟ يمنع تمرير ملف تالف إلى المونتاج."""
    import json as _j
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                              "format=duration,size:stream=codec_type",
                              "-of", "json", path], capture_output=True, text=True, timeout=60).stdout
        d = _j.loads(out or "{}")
        dur = float(d.get("format", {}).get("duration") or 0)
        size = int(d.get("format", {}).get("size") or 0)
        has_a = any(x.get("codec_type") == "audio" for x in d.get("streams", []))
        return has_a and dur > 0.4 and size > 2048, {"duration": dur, "bytes": size, "audio_stream": has_a}
    except Exception as e:
        return False, {"error": str(e)[:160]}


def build(timeline_path, out_path, audio=None, music=None, lut=None, srt=None, fps=24, w=1920, h=1080):
    if audio and not audio_valid(audio)[0]:
        raise SystemExit(f"AUDIO INVALID — refusing to build silent mp4: {audio} {audio_valid(audio)[1]}")
    tl = json.load(open(timeline_path, encoding="utf-8"))
    clips = [c for c in tl["clips"] if c.get("asset")]
    if not clips:
        raise SystemExit("لا توجد مقاطع بأصول — لم يُنتج ملف")
    inputs, filters, concat_in = [], [], []
    for i, c in enumerate(clips):
        inputs += ["-i", c["asset"]]
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
    aidx = midx = None
    if audio:
        cmd += ["-i", audio]; aidx = n
    if music:
        cmd += ["-stream_loop", "-1", "-i", music]; midx = n + (1 if audio else 0)

    # خريطة الصوت: كل الحالات تُخرج تدفقاً مسمّى [aout] لضمان وجود صوت في الملف
    if audio and music:
        fc += f";[{aidx}:a]volume=1.0[a1];[{midx}:a]volume=0.16[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=0,alimiter=limit=0.95[aout]"
        amap = "[aout]"
    elif audio:
        fc += f";[{aidx}:a]aresample=48000,alimiter=limit=0.95[aout]"
        amap = "[aout]"
    elif music:
        fc += f";[{midx}:a]volume=0.35,aresample=48000,alimiter=limit=0.95[aout]"
        amap = "[aout]"
    else:
        fc += ";[vc]anullsrc=r=48000:cl=stereo[aout]"
        amap = "[aout]"

    cmd += ["-filter_complex", fc, "-map", vout, "-map", amap]
    total = sum(float(c["duration"]) for c in clips)
    cmd += ["-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_path]
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    sh(cmd)
    ok, ainfo = audio_valid(out_path)
    return {"out": out_path, "clips": n, "fps": fps, "resolution": f"{w}x{h}",
            "audio_present": ok, "audio_probe": ainfo}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", default="05_edit/timeline.json")
    ap.add_argument("--out", default="05_edit/assembly_v1.mp4")
    ap.add_argument("--audio"); ap.add_argument("--music"); ap.add_argument("--lut"); ap.add_argument("--srt")
    a = ap.parse_args()
    print(json.dumps(build(a.timeline, a.out, a.audio, a.music, a.lut, a.srt), indent=1))
