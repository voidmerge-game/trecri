"""إحصاءات مشاهد محايدة — أرقام فقط، بلا أي حكم فني.

هذا هو الحد الأقصى المسموح. لا يولّد توصيات جمالية.
الاستخدام: python -m pipeline.grade.scene_stats 05_edit/preview.mp4 --out stats.csv
"""
import argparse, csv, json, os, subprocess, tempfile

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

def scene_cuts(path, threshold=0.35):
    out = run(["ffmpeg", "-i", path, "-filter:v", f"select='gt(scene,{threshold})',showinfo",
               "-f", "null", "-"])
    times = []
    for line in out.splitlines():
        if "pts_time:" in line:
            try: times.append(float(line.split("pts_time:")[1].split()[0]))
            except Exception: pass
    return times

def frame_stats(path, every=5):
    tmp = tempfile.mkdtemp()
    run(["ffmpeg", "-i", path, "-vf", f"fps=1/{every},scale=64:36", "-q:v", "5",
         os.path.join(tmp, "f%04d.jpg")])
    from PIL import Image
    rows = []
    for f in sorted(os.listdir(tmp)):
        im = Image.open(os.path.join(tmp, f)).convert("RGB")
        px = list(im.getdata()); n = len(px)
        r = sum(p[0] for p in px)/n/255; g = sum(p[1] for p in px)/n/255; b = sum(p[2] for p in px)/n/255
        rows.append({"frame": f, "mean_r": round(r,4), "mean_g": round(g,4), "mean_b": round(b,4),
                     "luma": round(0.2126*r+0.7152*g+0.0722*b,4)})
    return rows

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--out", default="stats.csv")
    a = ap.parse_args()
    cuts = scene_cuts(a.video); rows = frame_stats(a.video)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["frame"]); w.writeheader(); w.writerows(rows)
    print(json.dumps({"scene_cuts": len(cuts), "frames_sampled": len(rows), "csv": a.out}))
