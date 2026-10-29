"""استخراج أشخاص/أماكن بسيط + رسم SVG. يستخدم spaCy إن توفر، وإلا regex محافظ."""
import argparse, json, re

def extract(text):
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        people = sorted({e.text.strip() for e in doc.ents if e.label_ == "PERSON" and len(e.text) > 3})
        places = sorted({e.text.strip() for e in doc.ents if e.label_ in ("GPE", "LOC")})
        engine = "spacy:en_core_web_sm"
    except Exception:
        people = sorted(set(re.findall(r"\b(?:Mr|Mrs|Miss|Dr)\.?\s+[A-Z][a-z]+", text)))
        places = sorted(set(re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?,\s?(?:Mont|N\.Y|Cal|Ill)\.?", text)))
        engine = "regex-fallback"
    return {"engine": engine, "people": people, "places": places}

def to_svg(data, out, w=1400, h=800):
    people, places = data["people"], data["places"]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
         f'<rect width="{w}" height="{h}" fill="#0e1013"/>']
    def col(x, color, start_y=90):
        for i, name in enumerate(x[:14]):
            y = start_y + i*46
            p.append(f'<rect x="80" y="{y-22}" width="380" height="30" rx="4" fill="{color}"/>')
            p.append(f'<text x="94" y="{y}" fill="#e6e4de" font-size="16" font-family="Helvetica">{name[:40]}</text>')
    col(people, "#2a3038")
    p.append(f'<text x="80" y="56" fill="#8a929c" font-size="18" font-family="Helvetica">PEOPLE</text>')
    for i, name in enumerate(places[:14]):
        y = 90 + i*46
        p.append(f'<rect x="{w-460}" y="{y-22}" width="380" height="30" rx="4" fill="#33272a"/>')
        p.append(f'<text x="{w-446}" y="{y}" fill="#e6e4de" font-size="16" font-family="Helvetica">{name[:40]}</text>')
    p.append(f'<text x="{w-460}" y="56" fill="#8a929c" font-size="18" font-family="Helvetica">PLACES</text>')
    p.append(f'<text x="30" y="{h-20}" fill="#565e68" font-size="12" font-family="Helvetica">engine: {data["engine"]}</text>')
    p.append("</svg>")
    open(out, "w").write("\n".join(p)); return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("txt"); ap.add_argument("--json", default="graph.json"); ap.add_argument("--svg", default="graph.svg")
    a = ap.parse_args(); d = extract(open(a.txt, encoding="utf-8").read())
    json.dump(d, open(a.json, "w"), ensure_ascii=False, indent=1); to_svg(d, a.svg); print(json.dumps(d, ensure_ascii=False)[:300])
