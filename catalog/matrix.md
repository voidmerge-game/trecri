# catalog/matrix.md — matrix تنفيذ حقيقي (لا تقديرات)

> المصدر: تشغيل `tools-probe` رقم **40935718660** على GitHub Actions.
> ⚠️ `continue-on-error` يجعل الخطوة تظهر `success` حتى عند الفشل — لذلك كل حكم هنا **مقروء من اللوگ**، لا من اللون الأخضر.

| الوحدة | الحالة الحقيقية | الدليل من اللوگ | الإجراء |
|---|---|---|---|
| `auto-editor` | ✅ يعمل (ثنائي) | نزّل `auto-editor-linux-x86_64` بنجاح | سيُستخدم في `clean` |
| `demucs` | ❌ يفشل | `ModuleNotFoundError: No module named 'numpy'` | إصلاح: تثبيت numpy صريحاً |
| `iopaint` | ❌ يفشل (تثبيت) | `ERROR: Failed building wheel for Pillow` | إصلاح: pin numpy<2 + Pillow جاهز |
| `realesrgan` + `basicsr` | ❌ يفشل | `No module named 'torchvision.transforms.functional_tensor'` | إصلاح: `torchvision<0.17` |
| `gfpgan` | ❌ يفشل | نفس سبب basicsr | إصلاح: نفس الـ pin |
| `pedalboard` | ✅ يعمل | `pedalboard OK` | يُستخدم في `fx` |
| `chatterbox-tts` | ✅ قابل للتنزيل | `chatterbox_tts-0.1.7-py3-none-any.whl` | غير مُشغَّل (يحتاج أوزاناً) |
| `torch` | متوفر CPU | `torch 2.15.0+cu132 cuda False` | **لا GPU** — مؤكد |

## السبب الجذري الموحَّد
`basicsr` (الذي يعتمد عليه `gfpgan` و`realesrgan`) يستورد `torchvision.transforms.functional_tensor`، وقد **حُذف هذا الملف في torchvision ≥ 0.17**. أي تثبيت حديث يفشل.
**الحل المسجَّل:** `pip install "torchvision<0.17" "numpy<2"` قبل تثبيت أي منهما.

## ما لم يُختبر بعد
`ACE-Step` · `Stable Audio Open` · `MMAudio` · `Bark` · `Meshroom` — تحتاج GPU أو أوزاناً ثقيلة.
