"""تفكيك النص إلى shotlist.json — مشاهد ← لقطات، بلا تفسير إبداعي.

الاستخدام: python -m pipeline.script.breakdown 02_script/final.fountain 02_script/shotlist.json
"""
import json, os, sys, re
from pipeline.script.lint import parse

SHOT_TYPES = ["aerial", "wide", "medium", "close", "detail", "page", "map", "portrait"]

def breakdown(fountain_path):
    text = open(fountain_path, encoding="utf-8").read()
    scenes = parse(text)
    shots, sid, prev = [], 0, None
    for sc_i, s in enumerate(scenes, 1):
        body = " ".join(s["lines"])
        src = re.findall(r"\[SRC:\s*([^\]]+)\]", body)
        for j, line in enumerate(s["lines"], 1):
            if re.match(r"^[A-Z][A-Z0-9 \.'\-]{1,40}$", line) and len(line) > 2:
                continue  # اسم شخصية
            sid += 1
            kind = "page" if re.search(r"headline|newspaper|document|letter", line, re.I) else \
                   "map" if re.search(r"map|route|location", line, re.I) else \
                   "portrait" if re.search(r"portrait|face|photograph", line, re.I) else "wide"
            if kind == prev: kind = "medium"  # تفادي تكرار نفس النوع
            prev = kind
            shots.append({
                "shot_id": f"S{sid:03d}",
                "scene": sc_i,
                "heading": s["heading"],
                "index_in_scene": j,
                "type": kind,
                "text": line.strip(),
                "sources": src,
                "duration_hint_s": max(2.5, min(8.0, round(len(line.split()) / 3.0, 1))),
            })
    return {"generated_from": fountain_path, "scene_count": len(scenes),
            "shot_count": len(shots), "shots": shots}

if __name__ == "__main__":
    out = breakdown(sys.argv[1])
    d = os.path.dirname(sys.argv[2])
    if d: os.makedirs(d, exist_ok=True)
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"scenes={out['scene_count']} shots={out['shot_count']} -> {sys.argv[2]}")
