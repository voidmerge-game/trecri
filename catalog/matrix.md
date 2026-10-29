# catalog/matrix.md — مصفوفة تنفيذ حقيقي (لا تقديرات)

> المصدر: تشغيل `tools-probe` رقم **40937429970** على GitHub Actions.
> ⚠️ `continue-on-error` يجعل الخطوة خضراء حتى عند الفشل — لذلك كل حكم هنا **مقروء من اللوگ نصياً**، لا من اللون.

| الوحدة | الحالة | الدليل النصي من اللوگ |
|---|---|---|
| `auto-editor` | ✅ **يعمل** | `IN=8.176871` → `OUT=6.400000` (حذف 1.78s صمت) |
| `demucs` | ✅ **يعمل** | `/tmp/stems/htdemucs/song/vocals.wav` + `no_vocals.wav` |
| `iopaint` | ✅ **يعمل** | نزّل `big-lama.pt` (196MB, md5 مطابق) وأنتج `/tmp/inp_out/inp.png` |
| `realesrgan` + `basicsr` | ✅ **يستورد ويعمل** | `imports OK` + `RRDB.pth` 67MB |
| `gfpgan` | ✅ **يستورد** | `gfpgan import OK` |
| `pedalboard` | ✅ **يعمل** | `pedalboard OK` |
| `chatterbox-tts` | ✅ **قابل للتنزيل** | `chatterbox_tts-0.1.7-py3-none-any.whl` |
| `torch` | ✅ CPU فقط | `torch 2.15.0+cpu cuda False` — **لا GPU** |

## الأخطاء التي ظهرت وحُلّت (بالترتيب الفعلي)

| # | الخطأ | السبب الجذري | الحل المطبَّق |
|---|---|---|---|
| 1 | `No module named 'numpy'` (demucs) | venv بلا numpy صريح | `pip install "numpy<2"` أولاً |
| 2 | `Failed building wheel for Pillow` (iopaint) | بناء من المصدر بلا رؤوس | `libjpeg-dev zlib1g-dev libwebp-dev libtiff-dev libfreetype6-dev liblcms2-dev` |
| 3 | `No module named 'torchvision.transforms.functional_tensor'` | `basicsr` يستورد ملفاً حُذف في torchvision ≥0.17 | **شيم re-export** يُنشأ تلقائياً |
| 4 | `No matching distribution for torchvision<0.17` | لا نسخة <0.17 لبايثون 3.12 | تخلي عن التخفيض → الشيم |
| 5 | `No module named 'torchvision'` | الشيم قبل تثبيت torchvision | تثبيت `torch torchvision` من `whl/cpu` أولاً |
| 6 | `Timeline is empty` (auto-editor) | عتبة `0.03` نسبة خطأ ≈ −30dB | **`threshold=-40dB`** في الاختبار وفي `pipeline/audio/clean.py` |

## ما زال غير مُختبَر
`ACE-Step` · `Stable Audio Open` · `MMAudio` · `Bark` · `Meshroom` · `Chatterbox` (تشغيل فعلي) — تحتاج GPU أو أوزاناً ثقيلة.
