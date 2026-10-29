"""خط زمني SVG من JSON — بلا متصفح، بلا اعتماديات."""
import argparse, json

def render(events, out, w=1280, h=720):
    n = max(1, len(events))
    gap = (w - 200) / n
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
         f'<rect width="{w}" height="{h}" fill="#101214"/>',
         f'<line x1="100" y1="{h//2}" x2="{w-100}" y2="{h//2}" stroke="#3a4048" stroke-width="2"/>']
    for i, e in enumerate(events):
        x = 100 + gap * (i + 0.5)
        up = i % 2 == 0
        y1 = h//2 - 30 if up else h//2 + 30
        y2 = h//2 - 120 if up else h//2 + 120
        col = "#b4342f" if e.get("key") else "#8a929c"
        p.append(f'<line x1="{x:.0f}" y1="{y1}" x2="{x:.0f}" y2="{y2}" stroke="{col}" stroke-width="2"/>')
        p.append(f'<circle cx="{x:.0f}" cy="{h//2}" r="7" fill="{col}"/>')
        ytxt = y2 - 12 if up else y2 + 22
        p.append(f'<text x="{x:.0f}" y="{ytxt}" fill="#e8e6e1" font-size="20" font-family="Georgia,serif" text-anchor="middle">{e.get("date","")}</text>')
        for k, ln in enumerate(str(e.get("label","")).split("\n")):
            p.append(f'<text x="{x:.0f}" y="{ytxt + 22 + k*18}" fill="{col}" font-size="15" font-family="Helvetica,Arial" text-anchor="middle">{ln}</text>')
    p.append(f'<text x="40" y="{h-30}" fill="#5b636d" font-size="14" font-family="Helvetica">TIMELINE · reconstructed from archived sources</text>')
    p.append("</svg>")
    open(out, "w").write("\n".join(p))
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("json"); ap.add_argument("out")
    a = ap.parse_args(); print(render(json.load(open(a.json)), a.out))
