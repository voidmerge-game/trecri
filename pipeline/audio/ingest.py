"""استقبال التعليق الصوتي من الطرف الثالث: تحقق تقني بلا أي تحليل للمحتوى.

يفحص: المدة، القناة، معدل العينة، الذروة، الارتفاع الصوتي. أرقام فقط.
"""
import argparse, json, subprocess

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size:stream=channels,sample_rate,codec_name",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def loudness(path):
    p = subprocess.run(["ffmpeg", "-i", path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    tail = p.stderr.strip().splitlines()
    try:
        blob = "\n".join(tail[-14:])
        return json.loads(blob[blob.index("{"):blob.rindex("}")+1])
    except Exception:
        return {"error": "loudnorm parse failed"}

def check(path):
    d = probe(path); ln = loudness(path)
    dur = float(d["format"]["duration"])
    return {"file": path, "duration_s": round(dur, 2), "bytes": int(d["format"]["size"]),
            "codec": d["streams"][0].get("codec_name"), "channels": d["streams"][0].get("channels"),
            "sample_rate": d["streams"][0].get("sample_rate"),
            "integrated_lufs": ln.get("input_i"), "true_peak_db": ln.get("input_tp"),
            "verdict": "ACCEPTED" if dur > 1 and ln.get("input_i") not in (None, "-inf") else "REJECTED"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("wav"); ap.add_argument("--out", default="03_audio/ingest.json")
    a = ap.parse_args(); r = check(a.wav)
    json.dump(r, open(a.out, "w"), indent=1); print(json.dumps(r, indent=1))
    raise SystemExit(0 if r["verdict"] == "ACCEPTED" else 1)
