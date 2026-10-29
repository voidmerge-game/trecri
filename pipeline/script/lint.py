"""مدقق نص: بنية Fountain + قواعد إلزامية. لا يكتب نصاً — يفحص فقط.

الاستخدام: python -m pipeline.script.lint 02_script/final.fountain
يرجع 0 عند النجاح، 1 عند وجود أخطاء مانعة.
"""
import re, sys, json

INT_EXT = re.compile(r"^(INT|EXT|EST|INT\./EXT)[\. ].*", re.I)
TRANS = re.compile(r"^[A-Z ]+ TO:$")
CHAR = re.compile(r"^[A-Z][A-Z0-9 \.'\-]{1,40}$")
PAREN = re.compile(r"^\(.*\)$")

def parse(text):
    lines = text.splitlines()
    scenes = []
    cur = None
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if INT_EXT.match(line.strip()):
            cur = {"heading": line.strip(), "lines": [], "dialogue": [], "chars": set()}
            scenes.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
            if CHAR.match(line.strip()) and len(cur["lines"]) > 1:
                cur["chars"].add(line.strip())
            if PAREN.match(line.strip()):
                pass
    return scenes

def lint(path):
    text = open(path, encoding="utf-8").read()
    errs, warns = [], []
    scenes = parse(text)

    if not scenes:
        errs.append("لا يوجد أي عنوان مشهد (INT./EXT.) — النص ليس Fountain صالحاً")

    for i, s in enumerate(scenes, 1):
        h = s["heading"]
        if " - " not in h and "-" not in h.split(" ", 1)[-1]:
            warns.append(f"مشهد {i}: العنوان بلا موقع زمني صريح (DAY/NIGHT) — «{h[:60]}»")
        if len(s["lines"]) < 2:
            warns.append(f"مشهد {i}: قصير جداً ({len(s['lines'])} سطر)")
        if len(s["lines"]) > 60:
            warns.append(f"مشهد {i}: طويل ({len(s['lines'])} سطر) — قد يحتاج تفكيكاً")

    # كل ادعاء يحتاج مصدراً: نطلب مرجعاً بصيغة [SRC: ...] قرب كل مشهد سردي
    for i, s in enumerate(scenes, 1):
        body = "\n".join(s["lines"])
        if "[SRC:" not in body and "[SRC:" not in s["heading"]:
            warns.append(f"مشهد {i}: بلا مرجع مصدر [SRC: ...] — أي ادعاء فيه غير مسند")

    # العربية ممنوعة في أي نص يخص المنتج
    arb = re.findall(r"[\u0600-\u06FF]", text)
    if arb:
        errs.append(f"يوجد {len(arb)} حرفاً عربياً في النص — المنتج إنجليزي فقط")

    return {"scenes": len(scenes), "errors": errs, "warnings": warns,
            "chars": sorted({c for s in scenes for c in s["chars"]})}

if __name__ == "__main__":
    r = lint(sys.argv[1])
    print(json.dumps(r, ensure_ascii=False, indent=1))
    raise SystemExit(1 if r["errors"] else 0)
