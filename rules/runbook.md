# runbook — أوامر التشغيل

## المسارات
```
01_research/   ← pipeline.research.run
02_script/     ← pipeline.script.lint / breakdown
03_audio/      ← pipeline.audio.ingest / clean / fx
04_visuals/    ← pipeline.docs · pipeline.maps · pipeline.real · pipeline.restore
05_edit/       ← pipeline.edit.timeline_build / assemble / otio_export · pipeline.grade
06_final/      ← pipeline.final.deliver
```

## 1) البحث والأرشفة
```bash
gh workflow run research.yml -f query="<english query>" -f date_from=1902 -f date_to=1908 -f rows=6
```

## 2) النص
```bash
python3 -m pipeline.script.lint 02_script/final.fountain            # 0 = سليم
python3 -m pipeline.script.breakdown 02_script/final.fountain 02_script/shotlist.json
```

## 3) الصوت
```bash
python3 -m pipeline.audio.ingest 03_audio/narrator_raw.wav          # ACCEPTED / REJECTED
python3 -m pipeline.audio.clean 03_audio/narrator_raw.wav --out 03_audio/narrator_clean.wav
python3 -m pipeline.audio.fx 03_audio/line.wav 03_audio/line_phone.wav --kind phone
```

## 4) الوثائق والخرائط
```bash
python3 -m pipeline.docs.clipping  --headline "..." --body "..." --out 04_visuals/docs/clip.png
python3 -m pipeline.docs.handwriting "text" 04_visuals/docs/letter.png
python3 -m pipeline.docs.age 04_visuals/docs/clip.png 04_visuals/docs/clip_aged.png
python3 -m pipeline.maps.timeline events.json 04_visuals/maps/timeline.svg
python3 -m pipeline.maps.caseboard board.json 04_visuals/maps/caseboard.svg
python3 -m pipeline.maps.graph notes.txt --json 04_visuals/maps/graph.json --svg 04_visuals/maps/graph.svg
```

## 5) الترميم (ترتيب إلزامي)
```bash
python3 -m pipeline.restore.chain in.jpg 04_visuals/restored --colourise
```

## 6) المواد الحقيقية
```bash
python3 -m pipeline.real.broll "<english query>" --out 04_visuals/broll --limit 5
```

## 7) التلوين
```bash
python3 -m pipeline.grade.build_lut 05_edit/noir.cube --size 33
python3 -m pipeline.grade.look_extract ref.jpg --out 05_edit/look.json
```

## 8) التجميع والتسليم
```bash
python3 -m pipeline.edit.timeline_build --shotlist 02_script/shotlist.json --visuals 04_visuals --out 05_edit/timeline.json
python3 -m pipeline.edit.assemble --out 05_edit/assembly_v1.mp4 \
        --audio 03_audio/narrator_clean.wav --music 03_audio/music_bed.wav \
        --lut 05_edit/noir.cube --srt 05_edit/assembly.srt
python3 -m pipeline.edit.otio_export --timeline 05_edit/timeline.json --outdir 05_edit
python3 -m pipeline.final.deliver 05_edit/assembly_v1.mp4 --out 06_final/delivered.json
```

## حدود معروفة
- `freesound` و`pexels` تحتاج `FREESOUND_KEY` / `PEXELS_KEY` — بدونهما تُرجِع `MISSING_KEY`.
- `gfpgan` / `realesrgan` / `iopaint` تُسجَّل `SKIPPED` إن لم تكن مثبّتة.
- `meshroom` / `deoldify` / `pycapcut`: خارج المسار (السبب في `catalog/manifest.md`).
