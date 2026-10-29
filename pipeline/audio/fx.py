"""مؤثرات صوتية: هاتف/راديو/صدى. Pedalboard إن توفر، وإلا فلاتر FFmpeg المكافئة."""
import argparse, json, shutil, subprocess

def via_pedalboard(src, dst, kind):
    from pedalboard import Pedalboard, HighpassFilter, Distortion, Reverb, Compressor, Gain
    from pedalboard.io import AudioFile
    chain = {
        "phone": Pedalboard([HighpassFilter(300), HighpassFilter(3000), Distortion(drive_db=6), Compressor(threshold_db=-18, ratio=4), Gain(gain_db=-2)]),
        "radio": Pedalboard([HighpassFilter(500), Distortion(drive_db=10), Reverb(room_size=0.15, wet_level=0.08)]),
        "echo":  Pedalboard([Reverb(room_size=0.75, wet_level=0.28, damping=0.6)]),
    }[kind]
    with AudioFile(src) as f:
        audio = f.read(f.frames); sr = f.samplerate
    out = chain(audio, sr)
    with AudioFile(dst, "w", sr, out.shape[0]) as f:
        f.write(out)
    return {"engine": "pedalboard", "kind": kind, "out": dst}

FF = {
    "phone": "highpass=f=300,highpass=f=3000,acompressor=threshold=-18dB:ratio=4,volume=-2dB",
    "radio": "highpass=f=500,aeval=val(0)*3:val(1)*3,alimiter=limit=0.6",
    "echo":  "aecho=0.8:0.85:120|240:0.35|0.18",
}

def via_ffmpeg(src, dst, kind):
    subprocess.run(["ffmpeg", "-y", "-i", src, "-af", FF[kind], dst], check=True, capture_output=True)
    return {"engine": "ffmpeg", "kind": kind, "out": dst}

def apply(src, dst, kind):
    try:
        return via_pedalboard(src, dst, kind)
    except Exception as e:
        return via_ffmpeg(src, dst, kind) | {"fallback_reason": str(e)[:120]}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--kind", choices=["phone", "radio", "echo"], default="phone")
    a = ap.parse_args(); print(json.dumps(apply(a.src, a.dst, a.kind), indent=1))
