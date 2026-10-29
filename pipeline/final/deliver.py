"""تقرير التسليم: بيانات وصفية محايدة فقط. ⛔ لا تحليل ولا تقييم."""
import argparse, json, os, subprocess

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate",
        "-of", "json", path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--out", default="06_final/delivered.json")
    a = ap.parse_args()
    d = probe(a.video)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), {})
    au = next((s for s in d["streams"] if s["codec_type"] == "audio"), {})
    rep = {"file": a.video, "duration_s": round(float(d["format"]["duration"]), 2),
           "size_mb": round(int(d["format"]["size"]) / 1048576, 2),
           "resolution": f'{v.get("width")}x{v.get("height")}', "fps": v.get("r_frame_rate"),
           "video_codec": v.get("codec_name"), "audio_codec": au.get("codec_name"),
           "note": "metadata only — content review is the owner's, not the agent's"}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(rep, open(a.out, "w"), indent=1)
    print(json.dumps(rep, indent=1))

if __name__ == "__main__": main()
