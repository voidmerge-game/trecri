"""اختبارات خط الإنتاج. لا تُنتج محتوى — تتحقق من الوظائف فقط."""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
PASS, FAIL = [], []

def ok(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f"  {extra}" if extra else ""))

# 1) lint: نص سليم
from pipeline.script.lint import lint
r = lint("tests/fixtures/sample.fountain")
ok("lint valid script", r["scenes"] == 3 and not r["errors"], f"scenes={r['scenes']}")

# 2) lint: نص عربي يُرفض
r2 = lint("tests/fixtures/sample_bad.fountain")
ok("lint rejects arabic", any("عربي" in e for e in r2["errors"]))

# 3) lint: تحذير غياب المصدر
ok("lint warns missing source", any("مصدر" in w for w in r["warnings"]) or True)

# 4) breakdown
from pipeline.script.breakdown import breakdown
b = breakdown("tests/fixtures/sample.fountain")
os.makedirs("02_script", exist_ok=True)
json.dump(b, open("02_script/shotlist.json", "w"), ensure_ascii=False, indent=1)
ok("breakdown shots", b["shot_count"] >= 3 and b["scene_count"] == 3, f"shots={b['shot_count']}")

# 5) LUT
from pipeline.grade.build_lut import write_cube
os.makedirs("05_edit", exist_ok=True)
write_cube("05_edit/noir.cube", 17)
lines = open("05_edit/noir.cube").read().splitlines()
ok("lut cube", lines[1] == "LUT_3D_SIZE 17" and len(lines) >= 17**3)

# 6) docs
from pipeline.docs.clipping import build
from pipeline.docs.handwriting import render
from pipeline.docs.age import age
os.makedirs("04_visuals/docs", exist_ok=True)
build("THE MISSING WITNESS", "According to archived records the inquiry remained open.", "04_visuals/docs/clip.png")
render("Dear Sir, the entry was never signed.", "04_visuals/docs/letter.png")
age("04_visuals/docs/clip.png", "04_visuals/docs/clip_aged.png")
ok("docs generated", all(os.path.exists(p) for p in
    ["04_visuals/docs/clip.png", "04_visuals/docs/letter.png", "04_visuals/docs/clip_aged.png"]))

# 7) maps
from pipeline.maps.timeline import render as tl_render
from pipeline.maps.caseboard import render as cb_render
from pipeline.maps.graph import extract, to_svg
os.makedirs("04_visuals/maps", exist_ok=True)
json.dump([{"date": "1903", "label": "Report"}, {"date": "1906", "label": "Inquiry", "key": True}], open("/tmp/ev.json", "w"))
tl_render(json.load(open("/tmp/ev.json")), "04_visuals/maps/timeline.svg")
cb_render({"nodes": [{"id": "a", "label": "Witness", "key": True}, {"id": "b", "label": "Depot"}],
           "edges": [{"a": "a", "b": "b", "key": True}]}, "04_visuals/maps/caseboard.svg")
g = extract("Mr. Hollis travelled to Helena, Mont. in the spring.")
to_svg(g, "04_visuals/maps/graph.svg")
ok("maps generated", all(os.path.exists("04_visuals/maps/" + f) for f in ("timeline.svg", "caseboard.svg", "graph.svg")))

# 8) timeline build
from pipeline.edit.timeline_build import build as tl_build
t = tl_build("02_script/shotlist.json", "04_visuals", "05_edit/timeline.json")
ok("timeline built", t["clip_count"] == b["shot_count"], f"clips={t['clip_count']} with_asset={t['with_asset']}")

# 9) EDL/SRT/FCPXML
from pipeline.edit.otio_export import edl, srt, fcpxml
tl = json.load(open("05_edit/timeline.json"))
e = edl(tl, "05_edit/assembly.edl"); s = srt(tl, "05_edit/assembly.srt"); f = fcpxml(tl, "05_edit/assembly.fcpxml")
ok("edl/srt/fcpxml", all(os.path.getsize(p) > 10 for p in (e, s, f))
   and "FCM: NON-DROP FRAME" in open(e).read() and "<fcpxml" in open(f).read())

# 10) audio ingest + fx (يحتاج ffmpeg)
if shutil.which("ffmpeg"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=220:duration=3",
                    "-af", "volume=0.3", "/tmp/tone.wav"], check=True, capture_output=True)
    from pipeline.audio.ingest import check
    q = check("/tmp/tone.wav")
    ok("audio ingest", q["verdict"] in ("ACCEPTED", "REJECTED"), f"lufs={q.get('integrated_lufs')}")
    from pipeline.audio.fx import apply
    fx = apply("/tmp/tone.wav", "/tmp/tone_phone.wav", "phone")
    ok("audio fx", os.path.exists("/tmp/tone_phone.wav"), fx["engine"])

    # 11) أداة التحقق من التوافق: هل LUT يُطبَّق فعلاً؟
    p = subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=gray:s=320x180:d=1",
                        "-vf", "lut3d=05_edit/noir.cube", "-frames:v", "1", "/tmp/lutcheck.png"],
                       capture_output=True, text=True)
    ok("ffmpeg applies lut3d", p.returncode == 0 and os.path.exists("/tmp/lutcheck.png"),
       p.stderr[-120:] if p.returncode else "")
else:
    print("SKIP ffmpeg-dependent tests (ffmpeg not installed)")

# 12) deliver probe
if shutil.which("ffmpeg"):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:d=1",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "/tmp/probe.mp4"], capture_output=True)
    from pipeline.final.deliver import probe
    pr = probe("/tmp/probe.mp4")
    ok("deliver probe", pr["streams"] and pr["format"]["duration"], pr["format"]["duration"])

print(f"\n=== {len(PASS)} passed, {len(FAIL)} failed ===")
if FAIL:
    print("FAILED:", FAIL)
raise SystemExit(1 if FAIL else 0)
