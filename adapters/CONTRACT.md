# adapters — عقد موحّد لكل وحدة
# كل ملف محوّل مستقل: kind / install / entry / take / io / license / verified

## osint-index — jivoi/awesome-osint
id: osint-index
kind: meta
status: NOT_NEEDED
license: CC0-1.0
install: —
entry: research/checklist.md
input: هيكل التحقيق
output: قائمة تحقق
take: فهرسه فقط كمرجع لبناء قائمة تحقق تحقيقية — لا كود ولا تثبيت
verified: jivoi/awesome-osint | stars=30545 | license=NOASSERTION | pushed=2026-10-29

## maigret — Maigret
id: maigret
kind: cli
status: READY
license: MIT
install: pip install maigret
entry: maigret <user> --json simple
input: اسم مستعار واحد
output: JSON: حسابات موجودة
take: محرك تعداد الأسماء المستعارة عبر CLI وإخراج JSON بسيط
verified: soxoj/maigret | stars=39513 | license=MIT | pushed=2026-10-29

## spiderfoot — SpiderFoot
id: spiderfoot
kind: cli
status: READY
license: MIT
install: pip install spiderfoot
entry: sf.py -s <target> -m <modules> -o json
input: هدف/نطاق
output: JSON نتائج
take: وحدة جمع المعلومات + تصدير JSON قابل للتحليل
verified: smicallef/spiderfoot | stars=24049 | license=MIT | pushed=2026-04-13

## bellingcat-toolkit — Bellingcat Toolkit
id: bellingcat-toolkit
kind: meta
status: NOT_NEEDED
license: —
install: —
entry: research/checklist.md
input: —
output: قائمة تحقق
take: منهجيته: خطوات التحقق (تحديد زمن، تحديد موقع، بحث عكسي)
verified: non-github

## auto-archiver — Auto-Archiver
id: auto-archiver
kind: cli
status: READY
license: MIT
install: pip install auto-archiver
entry: auto-archiver --config feeds.csv
input: روابط المصادر
output: WACZ + بيان أرشفة
take: قدرة الأرشفة قبل الاختفاء: صفحة → WACZ + manifesto بالهاش
verified: bellingcat/auto-archiver | stars=1140 | license=MIT | pushed=2026-09-10

## chronicling-america — Chronicling America
id: chronicling-america
kind: api
status: READY
license: Public Domain
install: —
entry: loc.gov/collections/chronicling-america/?fo=json
input: كلمة/تاريخ/ولاية
output: JSON + JPEG/PDF
take: API البحث + صور الصفحات عالية الدقة + OCR المدمج
verified: non-github

## loc-api — libofcongress-mcp-server
id: loc-api
kind: python
status: REPLACED
license: Public Domain
install: requests
entry: client/loc_api.py
input: استعلام
output: JSON نتائج + صور
take: عميل HTTP مباشر لـ loc.gov بدل طبقة MCP
verified: non-github

## newspaper-ocr — Newspaper-OCR-V3
id: newspaper-ocr
kind: cli
status: REPLACED
license: —
install: apt install tesseract-ocr poppler-utils; pip install ocrmypdf
entry: ocrmypdf --sidecar out.txt in.pdf out.pdf
input: PDF/صورة
output: نص + hOCR + PDF نصي
take: Tesseract + ocrmypdf بدل الأداة المجهولة
verified: unverified-name

## screenplay-writer — ai-screenplay-writer
id: screenplay-writer
kind: internal
status: REPLACED
license: —
install: pip install fountain-py
entry: pipeline/script/lint.py
input: ملف fountain
output: تقرير أخطاء
take: بنية Fountain القياسية + مدقق استمرارية بسيط
verified: unverified-name

## story-engine — writers-room-story-engine
id: story-engine
kind: meta
status: REPLACED
license: —
install: —
entry: catalog/templates/beats.yaml
input: —
output: قالب بنية
take: قالب بنية القصة (beats) كبيانات
verified: unverified-name

## storymachine — STORYMACHINE
id: storymachine
kind: internal
status: REPLACED
license: —
install: —
entry: tests/script_lint.py
input: fountain
output: قائمة ملاحظات آلية
take: قواعد تشخيص آلية: طول مشهد، تكرار، غياب مصدر
verified: unverified-name

## scriptbreak — scriptbreak
id: scriptbreak
kind: internal
status: REPLACED
license: —
install: —
entry: pipeline/script/breakdown.py
input: fountain
output: shotlist.json
take: تفكيك fountain إلى مشاهد ولقطات JSON
verified: unverified-name

## sceneflow — SceneFlow
id: sceneflow
kind: internal
status: REPLACED
license: —
install: —
entry: pipeline/edit/bind_shots.py
input: shotlist + timeline
output: timeline موثّق
take: ربط shot_id بمقطع فيديو داخل timeline
verified: unverified-name

## chatterbox — Chatterbox
id: chatterbox
kind: python
status: GPU_ONLY
license: MIT
install: pip install chatterbox-tts
entry: adapter.run(text)->wav
input: نص إنجليزي
output: WAV
take: TTS لمقاطع قصيرة بصوت ثانوي (ليس الراوي)
verified: resemble-ai/chatterbox | stars=27406 | license=MIT | pushed=2026-07-21

## silma-tts — SILMA TTS
id: silma-tts
kind: none
status: NOT_NEEDED
license: غير مؤكد
install: —
entry: —
input: —
output: —
take: لا نأخذها — ترخيصها غير مؤكد
verified: unverified-name

## bark — Bark
id: bark
kind: python
status: GPU_ONLY
license: MIT
install: pip install bark
entry: bark --text '...' 
input: نص/وصف
output: WAV
take: همسات وتنهيدات كطبقات ambience قصيرة
verified: suno-ai/bark | stars=39288 | license=MIT | pushed=2024-08-19

## ace-step — ACE-Step 1.5
id: ace-step
kind: python
status: GPU_ONLY
license: Apache-2.0
install: pip install ace-step
entry: ace-step --prompt ... --duration 45
input: prompt موسيقي
output: WAV
take: موسيقى bed بطول 30–60 ثانية
verified: ace-step/ACE-Step | stars=4999 | license=Apache-2.0 | pushed=2026-02-15

## stable-audio — Stable Audio Open
id: stable-audio
kind: python
status: GPU_ONLY
license: Stability Community (NC)
install: pip install stable-audio-tools
entry: --prompt ... --seconds 30
input: prompt
output: WAV
take: حلقات ambience/طبقات جو (غير تجاري)
verified: Stability-AI/stable-audio-tools | stars=3895 | license=MIT | pushed=2026-10-24

## mmaudio — MMAudio
id: mmaudio
kind: python
status: GPU_ONLY
license: MIT
install: pip install mmaudio
entry: --video clip.mp4
input: فيديو
output: WAV متزامن
take: foley متزامن مع الحركة
verified: hkchengrex/MMAudio | stars=2299 | license=MIT | pushed=2026-02-23

## freesound — Freesound
id: freesound
kind: api
status: READY
license: CC0 / CC-BY
install: —
entry: freesound.org/apiv2/search/text/
input: كلمة/نوع
output: JSON + WAV + license
take: ملفات CC0 + بيانات الترخيص لكل ملف عبر API
verified: non-github

## freesound-mcp — freesound-mcp-server
id: freesound-mcp
kind: none
status: REPLACED
license: —
install: —
entry: client/freesound.py
input: —
output: —
take: فكرة الاستعلام فقط → تُنفَّذ بعميل HTTP
verified: unverified-name

## demucs — Demucs
id: demucs
kind: cli
status: CPU_OK
license: MIT
install: pip install demucs
entry: demucs -n htdemucs in.wav
input: ملف صوتي
output: 4 ملفات WAV
take: فصل stems (vocals/drums/bass/other) للتنظيف
verified: adefossez/demucs | stars=3465 | license=MIT | pushed=2026-10-26

## pedalboard — Pedalboard
id: pedalboard
kind: python
status: READY
license: GPL-3.0
install: pip install pedalboard
entry: pipeline/audio/fx.py
input: WAV
output: WAV معالَج
take: سلسلة مؤثرات: highpass + distortion + reverb = صوت هاتف/راديو/صدى
verified: spotify/pedalboard | stars=6388 | license=GPL-3.0 | pushed=2026-10-23

## music-prompts — awesome-music-prompts
id: music-prompts
kind: meta
status: NOT_NEEDED
license: —
install: —
entry: catalog/templates/music_prompts.yaml
input: —
output: موجهات
take: صيغ موجهات موسيقية جاهزة كبيانات
verified: unverified-name

## scanold — ScanOld
id: scanold
kind: internal
status: REPLACED
license: —
install: pip install pillow
entry: pipeline/docs/clipping.py
input: نص + صورة
output: PNG قصاصة معلَّمة re-created
take: مظهر القصاصة القديمة عبر Pillow (تدرّج، حافة، ورق)
verified: unverified-name

## handwriting — text-to-handwriting
id: handwriting
kind: python
status: READY
license: MIT
install: —
entry: pipeline/docs/handwriting.py
input: نص إنجليزي
output: PNG
take: مولّد خط يد إنجليزي على ورق
verified: pnshiralkar/text-to-handwriting | stars=56 | license=NONE | pushed=2021-05-20

## manuscript — synthetic-manuscript-generator
id: manuscript
kind: internal
status: REPLACED
license: —
install: pip install pillow opencv-python
entry: pipeline/docs/age.py
input: صورة
output: PNG معتّق
take: تعتيق: بقع، طيّات، تغيّر لون الحبر
verified: unverified-name

## kepler — kepler.gl
id: kepler
kind: python
status: READY
license: MIT
install: pip install keplergl
entry: keplergl python + headless screenshot
input: CSV إحداثيات
output: PNG/إطارات
take: خرائط مسارات متحركة + تصدير صورة/إطارات
verified: keplergl/kepler.gl | stars=12068 | license=MIT | pushed=2026-10-29

## qgis — QGIS
id: qgis
kind: cli
status: HEAVY
license: GPL-2.0
install: apt install qgis (ثقيل)
entry: qgis_process run <alg>
input: طبقة/إحداثيات
output: GeoJSON/PNG
take: حسابات جغرافية headless: مسافات، نطاقات، تحويل إحداثيات
verified: qgis/QGIS | stars=14737 | license=GPL-2.0 | pushed=2026-10-29

## mapillary — Mapillary
id: mapillary
kind: api
status: READY
license: BSD-2
install: pip install mapillary_tools
entry: mapillary_tools download --bbox ...
input: bbox
output: JPEG + metadata
take: صور شوارع للموقع عبر API
verified: mapillary/mapillary_tools | stars=317 | license=BSD-2-Clause | pushed=2026-10-27

## timelinejs — TimelineJS3
id: timelinejs
kind: node
status: READY
license: MPL-2.0
install: —
entry: timeline.json + headless screenshot
input: JSON أحداث
output: PNG إطار زمني
take: تخطيط الخط الزمني من JSON
verified: NUKnightLab/TimelineJS3 | stars=3230 | license=MPL-2.0 | pushed=2026-09-22

## rawgraphs — RAWGraphs
id: rawgraphs
kind: node
status: READY
license: Apache-2.0
install: —
entry: rawgraphs headless
input: CSV
output: SVG/PNG
take: أنواع رسوم + تصدير SVG
verified: rawgraphs/rawgraphs-app | stars=9047 | license=Apache-2.0 | pushed=2026-10-08

## caseboard — Win-Hao/caseboard
id: caseboard
kind: internal
status: NOT_NEEDED
license: —
install: pip install pillow
entry: pipeline/evidence/caseboard.py
input: عناصر + علاقات
output: SVG/PNG
take: فكرة لوحة الأدلة والخيوط → مولّد SVG داخلي
verified: unverified-name

## social-graph — osint-social-graph-agent
id: social-graph
kind: python
status: REPLACED
license: —
install: pip install spacy networkx
entry: pipeline/evidence/graph.py
input: نص
output: JSON + SVG
take: NER (spaCy) + networkx لاستخراج أشخاص/أماكن ورسم علاقات
verified: unverified-name

## meshroom — Meshroom
id: meshroom
kind: none
status: NOT_NEEDED
license: MPL-2.0
install: —
entry: —
input: —
output: —
take: لا نأخذها — تحتاج GPU + واجهة Qt؛ البديل لوحة إيزومترية SVG
verified: alicevision/Meshroom | stars=13053 | license=NOASSERTION | pushed=2026-10-29

## forensics-3d — AI-Forensics-3D-Reconstruction
id: forensics-3d
kind: none
status: NOT_NEEDED
license: —
install: —
entry: —
input: —
output: —
take: لا نأخذها — لا مستودع مطابق؛ البديل رسم SVG / Blender headless
verified: unverified-name

## gfpgan — GFPGAN
id: gfpgan
kind: python
status: GPU_ONLY
license: Apache-2.0
install: pip install gfpgan
entry: gfpgan -i in.jpg -o out.jpg
input: صورة
output: صورة مرمّمة
take: ترميم الوجه — أول خطوة قبل التكبير
verified: TencentARC/GFPGAN | stars=37701 | license=NOASSERTION | pushed=2024-07-26

## realesrgan — Real-ESRGAN
id: realesrgan
kind: python
status: GPU_ONLY
license: BSD-3
install: pip install realesrgan
entry: realesrgan-ncnn-vulkan -i in -o out
input: صورة
output: صورة مكبّرة
take: تكبير 2×/4× بعد الترميم
verified: xinntao/Real-ESRGAN | stars=37266 | license=BSD-3-Clause | pushed=2024-08-06

## deoldify — DeOldify
id: deoldify
kind: none
status: NOT_NEEDED
license: MIT
install: —
entry: —
input: —
output: —
take: لا نأخذها — تبعيات مهجورة؛ البديل تلوين OpenCV + إفصاح Colourised
verified: jantic/DeOldify | stars=18454 | license=MIT | pushed=2024-10-19

## iopaint — IOPaint
id: iopaint
kind: python
status: CPU_OK
license: Apache-2.0
install: pip install iopaint
entry: iopaint run --model=lama
input: صورة + قناع
output: صورة منظّفة
take: inpainting لإزالة خدوش/عناصر غير مرغوبة
verified: Sanster/IOPaint | stars=23293 | license=Apache-2.0 | pushed=2025-04-29

## openmontage — OpenMontage
id: openmontage
kind: api
status: REPLACED
license: —
install: —
entry: client/archive_org.py / commons.py
input: استعلام
output: ملفات + تراخيص
take: فكرة المونتاج الأرشيفي → Archive.org + Wikimedia APIs
verified: unverified-name

## broll — broll-fetcher
id: broll
kind: api
status: REPLACED
license: —
install: —
entry: client/pexels.py
input: استعلام
output: MP4 + LICENSE + CREDITS
take: لقطات Pexels/Pixabay + ملف ترخيص لكل ملف
verified: unverified-name

## ffmpeg — FFmpeg
id: ffmpeg
kind: cli
status: READY
license: LGPL / GPL
install: apt install ffmpeg
entry: ffmpeg ...
input: أي وسيط
output: أي وسيط
take: كل عمليات الوسائط: trim, concat, zoompan, lut3d, loudnorm, subtitles
verified: FFmpeg/FFmpeg | stars=66037 | license=NOASSERTION | pushed=2026-10-29

## kburns — kburns-slideshow
id: kburns
kind: internal
status: REPLACED
license: —
install: —
entry: ffmpeg -vf zoompan=...
input: صورة ثابتة
output: MP4 بحركة
take: بارامترات حركة zoompan (مدة، اتجاه، تكبير)
verified: unverified-name

## remotion — Remotion
id: remotion
kind: node
status: READY
license: Remotion License ⚠️
install: npm i remotion @remotion/cli
entry: npx remotion render
input: props JSON
output: PNG seq / MP4
take: عناوين وخرائط وخط زمني كـ React → تسلسل PNG
verified: remotion-dev/remotion | stars=68835 | license=NOASSERTION | pushed=2026-10-29

## auto-editor — auto-editor
id: auto-editor
kind: cli
status: READY
license: Unlicense
install: pip install auto-editor
entry: auto-editor in.wav --edit audio
input: WAV
output: WAV مقصوص
take: قصّ الصمت من التعليق الصوتي
verified: WyattBlue/auto-editor | stars=5658 | license=Unlicense | pushed=2026-10-28

## pycapcut — pyCapCut
id: pycapcut
kind: none
status: NOT_NEEDED
license: —
install: —
entry: —
input: —
output: —
take: لا نأخذها — صيغة مغلقة؛ البديل OTIO → FCPXML + EDL + SRT
verified: unverified-name

## chromashift — ChromaShift
id: chromashift
kind: internal
status: REPLACED
license: —
install: pip install numpy
entry: pipeline/grade/build_lut.py
input: معاملات
output: LUT .cube
take: توليد ملف .cube: تباين، teal/orange، حبيبات، halation
verified: unverified-name

## deep-analog — deep-analog
id: deep-analog
kind: internal
status: REPLACED
license: —
install: pip install numpy pillow
entry: pipeline/grade/look_extract.py
input: صورة مرجعية
output: LUT .cube
take: استخراج LUT ثلاثي الأبعاد من صورة مرجعية
verified: unverified-name

## cinegrade — CinegradeAI
id: cinegrade
kind: internal
status: NOT_NEEDED
license: —
install: pip install numpy
entry: pipeline/grade/scene_stats.py
input: إطارات
output: CSV أرقام
take: إحصاءات مشاهد محايدة فقط (بدون أي حكم)
verified: unverified-name
