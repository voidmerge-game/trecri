"""تصدير مشروع قابل للتعديل: EDL (CMX3600) + FCPXML + SRT.

بديل مسجَّل لـ pyCapCut (صيغته مغلقة). هذه الصيغ يستوردها CapCut وResolve وPremiere.
"""
import argparse, json, os

def tc(sec, fps=24):
    f = int(round(sec * fps)); h, f = divmod(f, fps * 3600); m, f = divmod(f, fps * 60); s, f = divmod(f, fps)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"

def edl(tl, out):
    lines = ["TITLE: TR-ASSEMBLY", "FCM: NON-DROP FRAME", ""]
    rec = 0.0
    for i, c in enumerate([x for x in tl["clips"] if x.get("asset")], 1):
        d = float(c["duration"])
        lines.append(f"{i:03d}  AX       V     C        {tc(0)} {tc(d)} {tc(rec)} {tc(rec+d)}")
        lines.append(f"* FROM CLIP NAME: {os.path.basename(c['asset'])}")
        lines.append(f"* COMMENT: {c['shot_id']} {c['type']}")
        lines.append("")
        rec += d
    open(out, "w").write("\n".join(lines)); return out

def srt(tl, out):
    rec, n = 0.0, 1
    def t(sec):
        h, r = divmod(int(sec), 3600); m, s = divmod(r, 60); ms = int((sec - int(sec)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    blocks = []
    for c in [x for x in tl["clips"] if x.get("asset")]:
        d = float(c["duration"]); txt = (c.get("text") or "").strip()
        if txt:
            blocks.append(f"{n}\n{t(rec)} --> {t(rec+d)}\n{txt}\n"); n += 1
        rec += d
    open(out, "w", encoding="utf-8").write("\n".join(blocks)); return out

def fcpxml(tl, out, fps=24, w=1920, h=1080):
    clips = [x for x in tl["clips"] if x.get("asset")]
    total = sum(float(c["duration"]) for c in clips)
    def rat(sec): return f"{int(round(sec*fps))}/{fps}s"
    assets, items, rec = [], [], 0.0
    for i, c in enumerate(clips, 1):
        assets.append(f'<asset id="r{i}" name="{os.path.basename(c["asset"])}" start="0s" duration="{rat(float(c["duration"]))}" hasVideo="1" format="r0"/>')
        items.append(f'<asset-clip ref="r{i}" offset="{rat(rec)}" start="0s" duration="{rat(float(c["duration"]))}" name="{c["shot_id"]}"/>')
        rec += float(c["duration"])
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.9">
  <resources>
    <format id="r0" name="FFVideoFormat1080p{fps}" frameDuration="1/{fps}s" width="{w}" height="{h}"/>
    {"".join(assets)}
  </resources>
  <library><event name="TR"><project name="assembly">
    <sequence format="r0" duration="{rat(total)}" tcStart="0s">
      <spine>{"".join(items)}</spine>
    </sequence>
  </project></event></library>
</fcpxml>'''
    open(out, "w", encoding="utf-8").write(xml); return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--timeline", default="05_edit/timeline.json")
    ap.add_argument("--outdir", default="05_edit"); ap.add_argument("--name", default="assembly")
    a = ap.parse_args()
    tl = json.load(open(a.timeline, encoding="utf-8"))
    os.makedirs(a.outdir, exist_ok=True)
    print(edl(tl, os.path.join(a.outdir, a.name + ".edl")))
    print(srt(tl, os.path.join(a.outdir, a.name + ".srt")))
    print(fcpxml(tl, os.path.join(a.outdir, a.name + ".fcpxml")))
