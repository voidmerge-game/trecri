"""لوحة أدلة SVG: عناصر + خيوط حمراء للعناصر الجوهرية فقط."""
import argparse, json, math

def render(data, out, w=1600, h=900):
    nodes = data.get("nodes", []); edges = data.get("edges", [])
    cx, cy, R = w/2, h/2, min(w, h)/2 - 120
    pos = {}
    for i, n in enumerate(nodes):
        a = 2*math.pi*i/max(1, len(nodes))
        pos[n["id"]] = (cx + R*math.cos(a), cy + R*math.sin(a))
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
         f'<rect width="{w}" height="{h}" fill="#0e1013"/>']
    for e in edges:
        if e["a"] in pos and e["b"] in pos:
            x1, y1 = pos[e["a"]]; x2, y2 = pos[e["b"]]
            col = "#b4342f" if e.get("key") else "#39404a"
            wd = 3 if e.get("key") else 1.4
            p.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-width="{wd}" opacity="0.85"/>')
    for n in nodes:
        x, y = pos[n["id"]]
        rad = 12 if n.get("key") else 8
        fill = "#b4342f" if n.get("key") else "#2a3038"
        p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="{fill}" stroke="#7d858f" stroke-width="1.5"/>')
        p.append(f'<text x="{x:.0f}" y="{y - rad - 8:.0f}" fill="#dcdad4" font-size="15" font-family="Helvetica" text-anchor="middle">{n.get("label", n["id"])}</text>')
    p.append(f'<text x="30" y="{h-24}" fill="#565e68" font-size="13" font-family="Helvetica">EVIDENCE BOARD · derived from archived sources only</text>')
    p.append("</svg>")
    open(out, "w").write("\n".join(p))
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("json"); ap.add_argument("out")
    a = ap.parse_args(); print(render(json.load(open(a.json)), a.out))
