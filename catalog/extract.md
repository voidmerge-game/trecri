# extract — ما نأخذه من كل أداة

> لا نستنسخ أدوات. نأخذ منها **القدرة المحددة** التي تخدم الخط، ونترك الباقي.

| # | الأداة | ما نأخذه بالضبط | نوع التكامل |
|---|---|---|---|
| 1 | **jivoi/awesome-osint** | فهرسه فقط كمرجع لبناء قائمة تحقق تحقيقية — لا كود ولا تثبيت | `meta` |
| 2 | **Maigret** | محرك تعداد الأسماء المستعارة عبر CLI وإخراج JSON بسيط | `cli` |
| 3 | **SpiderFoot** | وحدة جمع المعلومات + تصدير JSON قابل للتحليل | `cli` |
| 4 | **Bellingcat Toolkit** | منهجيته: خطوات التحقق (تحديد زمن، تحديد موقع، بحث عكسي) | `meta` |
| 5 | **Auto-Archiver** | قدرة الأرشفة قبل الاختفاء: صفحة → WACZ + manifesto بالهاش | `cli` |
| 6 | **Chronicling America** | API البحث + صور الصفحات عالية الدقة + OCR المدمج | `api` |
| 7 | **libofcongress-mcp-server** | عميل HTTP مباشر لـ loc.gov بدل طبقة MCP | `python` |
| 8 | **Newspaper-OCR-V3** | Tesseract + ocrmypdf بدل الأداة المجهولة | `cli` |
| 9 | **ai-screenplay-writer** | بنية Fountain القياسية + مدقق استمرارية بسيط | `internal` |
| 10 | **writers-room-story-engine** | قالب بنية القصة (beats) كبيانات | `meta` |
| 11 | **STORYMACHINE** | قواعد تشخيص آلية: طول مشهد، تكرار، غياب مصدر | `internal` |
| 12 | **scriptbreak** | تفكيك fountain إلى مشاهد ولقطات JSON | `internal` |
| 13 | **SceneFlow** | ربط shot_id بمقطع فيديو داخل timeline | `internal` |
| 14 | **Chatterbox** | TTS لمقاطع قصيرة بصوت ثانوي (ليس الراوي) | `python` |
| 15 | **SILMA TTS** | لا نأخذها — ترخيصها غير مؤكد | `none` |
| 16 | **Bark** | همسات وتنهيدات كطبقات ambience قصيرة | `python` |
| 17 | **ACE-Step 1.5** | موسيقى bed بطول 30–60 ثانية | `python` |
| 18 | **Stable Audio Open** | حلقات ambience/طبقات جو (غير تجاري) | `python` |
| 19 | **MMAudio** | foley متزامن مع الحركة | `python` |
| 20 | **Freesound** | ملفات CC0 + بيانات الترخيص لكل ملف عبر API | `api` |
| 21 | **freesound-mcp-server** | فكرة الاستعلام فقط → تُنفَّذ بعميل HTTP | `none` |
| 22 | **Demucs** | فصل stems (vocals/drums/bass/other) للتنظيف | `cli` |
| 23 | **Pedalboard** | سلسلة مؤثرات: highpass + distortion + reverb = صوت هاتف/راديو/صدى | `python` |
| 24 | **awesome-music-prompts** | صيغ موجهات موسيقية جاهزة كبيانات | `meta` |
| 25 | **ScanOld** | مظهر القصاصة القديمة عبر Pillow (تدرّج، حافة، ورق) | `internal` |
| 26 | **text-to-handwriting** | مولّد خط يد إنجليزي على ورق | `python` |
| 27 | **synthetic-manuscript-generator** | تعتيق: بقع، طيّات، تغيّر لون الحبر | `internal` |
| 28 | **kepler.gl** | خرائط مسارات متحركة + تصدير صورة/إطارات | `python` |
| 29 | **QGIS** | حسابات جغرافية headless: مسافات، نطاقات، تحويل إحداثيات | `cli` |
| 30 | **Mapillary** | صور شوارع للموقع عبر API | `api` |
| 31 | **TimelineJS3** | تخطيط الخط الزمني من JSON | `node` |
| 32 | **RAWGraphs** | أنواع رسوم + تصدير SVG | `node` |
| 33 | **Win-Hao/caseboard** | فكرة لوحة الأدلة والخيوط → مولّد SVG داخلي | `internal` |
| 34 | **osint-social-graph-agent** | NER (spaCy) + networkx لاستخراج أشخاص/أماكن ورسم علاقات | `python` |
| 35 | **Meshroom** | لا نأخذها — تحتاج GPU + واجهة Qt؛ البديل لوحة إيزومترية SVG | `none` |
| 36 | **AI-Forensics-3D-Reconstruction** | لا نأخذها — لا مستودع مطابق؛ البديل رسم SVG / Blender headless | `none` |
| 37 | **GFPGAN** | ترميم الوجه — أول خطوة قبل التكبير | `python` |
| 38 | **Real-ESRGAN** | تكبير 2×/4× بعد الترميم | `python` |
| 39 | **DeOldify** | لا نأخذها — تبعيات مهجورة؛ البديل تلوين OpenCV + إفصاح Colourised | `none` |
| 40 | **IOPaint** | inpainting لإزالة خدوش/عناصر غير مرغوبة | `python` |
| 41 | **OpenMontage** | فكرة المونتاج الأرشيفي → Archive.org + Wikimedia APIs | `api` |
| 42 | **broll-fetcher** | لقطات Pexels/Pixabay + ملف ترخيص لكل ملف | `api` |
| 43 | **FFmpeg** | كل عمليات الوسائط: trim, concat, zoompan, lut3d, loudnorm, subtitles | `cli` |
| 44 | **kburns-slideshow** | بارامترات حركة zoompan (مدة، اتجاه، تكبير) | `internal` |
| 45 | **Remotion** | عناوين وخرائط وخط زمني كـ React → تسلسل PNG | `node` |
| 46 | **auto-editor** | قصّ الصمت من التعليق الصوتي | `cli` |
| 47 | **pyCapCut** | لا نأخذها — صيغة مغلقة؛ البديل OTIO → FCPXML + EDL + SRT | `none` |
| 48 | **ChromaShift** | توليد ملف .cube: تباين، teal/orange، حبيبات، halation | `internal` |
| 49 | **deep-analog** | استخراج LUT ثلاثي الأبعاد من صورة مرجعية | `internal` |
| 50 | **CinegradeAI** | إحصاءات مشاهد محايدة فقط (بدون أي حكم) | `internal` |

## أنواع التكامل

- `cli` — أداة سطر أوامر تُثبّت وتُنفَّذ مباشرة.
- `python` — حزمة تُستدعى من داخل السكربت.
- `node` — حزمة Node/React تُصيَّر headless.
- `api` — واجهة HTTP رسمية بلا تثبيت.
- `internal` — سلوك نكتبه بأنفسنا (بديل مسجَّل).
- `meta` — بيانات/قوالب لا كود.
- `none` — لا نأخذ شيئاً (السبب في manifest).

## القاعدة

**لا نأخذ من الأداة إلا ما يخدم مخرجاً محدداً في الخط.** أي قدرة لا تخدم مخرجاً = لا تُضمَّن.
