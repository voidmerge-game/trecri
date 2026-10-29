# manifest — الوحدات المطلوبة (50)

> المصدر الآلي: `catalog/units.json`. لا تُغيَّر حالة إلا بدليل تشغيل.

## الخلاصة

| الحالة | العدد |
|---|---|
| `REPLACED` | 16 |
| `READY` | 14 |
| `NOT_NEEDED` | 10 |
| `GPU_ONLY` | 7 |
| `CPU_OK` | 2 |
| `HEAVY` | 1 |

**المجموع: 50**

---

## الجدول الكامل

| # | الوحدة | الدور | الحالة | الرخصة | البديل | السبب إن لم نحتجها |
|---|---|---|---|---|---|---|
| 1 | **jivoi/awesome-osint** | فهرس مصادر تحقيق | `NOT_NEEDED` | CC0-1.0 | — | ليست أداة: قائمة قراءة. لا يوجد شيء يُثبَّت أو يُشغَّل. |
| 2 | **Maigret** | بحث عن حسابات بأسماء مستعارة | `READY` | MIT | — | — |
| 3 | **SpiderFoot** | أتمتة جمع معلومات | `READY` | MIT | — | — |
| 4 | **Bellingcat Toolkit** | منهجية تحقق | `NOT_NEEDED` | — | — | ليست أداة: منهجية مكتوبة. لا كود. |
| 5 | **Auto-Archiver** | أرشفة مصدر قبل اختفائه | `READY` | MIT | — | — |
| 6 | **Chronicling America** | قصاصات صحف تاريخية حقيقية | `READY` | Public Domain | — | — |
| 7 | **libofcongress-mcp-server** | ربط بأرشيف مكتبة الكونغرس | `REPLACED` | Public Domain | عميل HTTP مباشر | — |
| 8 | **Newspaper-OCR-V3** | استخراج نص من مسح ضوئي | `REPLACED` | — | tesseract + ocrmypdf | — |
| 9 | **ai-screenplay-writer** | كتابة مشاهد + تدقيق استمرارية | `REPLACED` | — | fountain parser | — |
| 10 | **writers-room-story-engine** | بنية قصة وأقواس شخصيات | `REPLACED` | — | سكربت بنية محلي | — |
| 11 | **STORYMACHINE** | تشخيص نص وتحسينه | `REPLACED` | — | linter محلي | — |
| 12 | **scriptbreak** | تفكيك نص إلى مشاهد ولقطات | `REPLACED` | — | fountain → shotlist.json | — |
| 13 | **SceneFlow** | مطابقة نص مع فيديو | `REPLACED` | — | shotlist ↔ timeline | — |
| 14 | **Chatterbox** | صوت ثانوي لمقاطع قصيرة | `GPU_ONLY` | MIT | — | — |
| 15 | **SILMA TTS** | صوت ثانٍ لمقتطفات وثائق | `NOT_NEEDED` | غير مؤكد | edge-tts / piper | الهوية والترخيص غير مؤكدين — لا تُدرج وحدة مجهولة الترخيص. |
| 16 | **Bark** | همسات وتنهيدات | `GPU_ONLY` | MIT | — | — |
| 17 | **ACE-Step 1.5** | موسيقى تصويرية | `GPU_ONLY` | Apache-2.0 | — | — |
| 18 | **Stable Audio Open** | أجواء وطبقات صوتية | `GPU_ONLY` | Stability Community (NC) | — | — |
| 19 | **MMAudio** | مؤثرات متزامنة مع الحركة | `GPU_ONLY` | MIT | — | — |
| 20 | **Freesound** | مؤثرات حقيقية | `READY` | CC0 / CC-BY | — | — |
| 21 | **freesound-mcp-server** | ربط بـ Freesound | `REPLACED` | — | عميل HTTP مباشر | — |
| 22 | **Demucs** | فصل صوت وتنظيف | `CPU_OK` | MIT | — | — |
| 23 | **Pedalboard** | رنين هاتف / تشويش راديو / صدى | `READY` | GPL-3.0 | — | — |
| 24 | **awesome-music-prompts** | موجهات موسيقية | `NOT_NEEDED` | — | — | ليست أداة: ملف نصوص. يُنسخ كبيانات عند الحاجة. |
| 25 | **ScanOld** | قصاصات مصنّعة تُعلَّم re-created | `REPLACED` | — | Pillow ageing | — |
| 26 | **text-to-handwriting** | رسائل بخط اليد بالإنجليزية | `READY` | MIT | — | — |
| 27 | **synthetic-manuscript-generator** | تعتيق ورق بحبر وطيّات وبقع | `REPLACED` | — | Pillow + OpenCV | — |
| 28 | **kepler.gl** | مسارات متحركة | `READY` | MIT | — | — |
| 29 | **QGIS** | تحليل جغرافي | `HEAVY` | GPL-2.0 | — | — |
| 30 | **Mapillary** | صور شوارع للمواقع | `READY` | BSD-2 | — | — |
| 31 | **TimelineJS3** | خط زمني | `READY` | MPL-2.0 | — | — |
| 32 | **RAWGraphs** | رسوم بيانية | `READY` | Apache-2.0 | — | — |
| 33 | **Win-Hao/caseboard** | لوحة أدلة وخيوط علاقات | `NOT_NEEDED` | — | مولّد SVG | المستودع بهذا الاسم غير موجود. البديل الصادق: مولّد SVG داخلي. |
| 34 | **osint-social-graph-agent** | استخراج أشخاص وأماكن ورسم علاقات | `REPLACED` | — | spaCy NER + networkx | — |
| 35 | **Meshroom** | مسح مواقع من صور متعددة | `NOT_NEEDED` | MPL-2.0 | لوحة إيزومترية ثابتة | يحتاج GPU + واجهة Qt — لا يعمل headless في Actions. ولا تتوفر صور مسح أصلاً. |
| 36 | **AI-Forensics-3D-Reconstruction** | تمثيل صامت | `NOT_NEEDED` | — | رسم SVG / blender headless | لا مستودع مطابق بهذا الاسم. |
| 37 | **GFPGAN** | ترميم وجوه (أولاً) | `GPU_ONLY` | Apache-2.0 | — | — |
| 38 | **Real-ESRGAN** | تكبير (ثانياً) | `GPU_ONLY` | BSD-3 | — | — |
| 39 | **DeOldify** | تلوين (أخيراً وبإفصاح) | `NOT_NEEDED` | MIT | opencv + إفصاح | تبعيات مهجورة (TF/PyTorch متعارضان) — أعلى احتمال فشل تثبيت في القائمة. |
| 40 | **IOPaint** | إزالة عيوب وعناصر | `CPU_OK` | Apache-2.0 | — | — |
| 41 | **OpenMontage** | لقطات من Archive.org وWikimedia | `REPLACED` | — | Archive.org API + Commons API | — |
| 42 | **broll-fetcher** | لقطات Pexels/Pixabay + تراخيص | `REPLACED` | — | Pexels API + CREDITS | — |
| 43 | **FFmpeg** | الأساس | `READY` | LGPL / GPL | — | — |
| 44 | **kburns-slideshow** | حركة صور ثابتة | `REPLACED` | — | ffmpeg zoompan | — |
| 45 | **Remotion** | عناوين وخرائط وخط زمني | `READY` | Remotion License ⚠️ | — | — |
| 46 | **auto-editor** | حذف الصمت | `READY` | Unlicense | — | — |
| 47 | **pyCapCut** | تسليم مشروع قابل للتعديل | `NOT_NEEDED` | — | OpenTimelineIO → FCPXML + EDL | صيغة CapCut مغلقة وغير موثّقة — لا يمكن ضمان التوافق. |
| 48 | **ChromaShift** | بناء LUT + حبيبات | `REPLACED` | — | مولّد .cube + ffmpeg lut3d | — |
| 49 | **deep-analog** | استخراج إطلالة من صورة مرجعية | `REPLACED` | — | look_extract.py | — |
| 50 | **CinegradeAI** | قياس مشاهد واقتراح تصحيح | `NOT_NEEDED` | — | scene_stats.py (أرقام فقط) | لا مستودع مطابق. |

---

## ما لا نحتاجه — صراحةً

- **jivoi/awesome-osint** — ليست أداة: قائمة قراءة. لا يوجد شيء يُثبَّت أو يُشغَّل.
- **Bellingcat Toolkit** — ليست أداة: منهجية مكتوبة. لا كود.
- **SILMA TTS** — الهوية والترخيص غير مؤكدين — لا تُدرج وحدة مجهولة الترخيص.
- **awesome-music-prompts** — ليست أداة: ملف نصوص. يُنسخ كبيانات عند الحاجة.
- **Win-Hao/caseboard** — المستودع بهذا الاسم غير موجود. البديل الصادق: مولّد SVG داخلي.
- **Meshroom** — يحتاج GPU + واجهة Qt — لا يعمل headless في Actions. ولا تتوفر صور مسح أصلاً.
- **AI-Forensics-3D-Reconstruction** — لا مستودع مطابق بهذا الاسم.
- **DeOldify** — تبعيات مهجورة (TF/PyTorch متعارضان) — أعلى احتمال فشل تثبيت في القائمة.
- **pyCapCut** — صيغة CapCut مغلقة وغير موثّقة — لا يمكن ضمان التوافق.
- **CinegradeAI** — لا مستودع مطابق.

## تنبيهات تراخيص إلزامية

- **Stable Audio Open** — رخصة غير تجارية.
- **Remotion** — غير مفتوحة المصدر.
- **Pedalboard / QGIS** — GPL.
- **FFmpeg** — تحقق من خيار GPL في البناء.
- **Freesound** — CC-BY يوجب الإسناد.
