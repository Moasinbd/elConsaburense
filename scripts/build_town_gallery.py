#!/usr/bin/env python3
"""Optimiza fotografías reales de Consuegra y evita dependencias externas si se descargan."""
from __future__ import annotations

import io
import pathlib
import time
import urllib.request
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "media" / "consuegra"
HTML = ROOT / "public" / "index.html"
OUT.mkdir(parents=True, exist_ok=True)

PHOTOS = [
    ("molinos", [
        "https://upload.wikimedia.org/wikipedia/commons/e/e0/Windmills_and_castle_of_Consuegra_%287079301421%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Windmills_and_castle_of_Consuegra_%287079301421%29.jpg/1280px-Windmills_and_castle_of_Consuegra_%287079301421%29.jpg",
    ]),
    ("castillo", [
        "https://upload.wikimedia.org/wikipedia/commons/9/9d/Castillo_de_Consuegra.jpg",
    ]),
    ("iglesia-san-juan", [
        "https://live.staticflickr.com/8896/18329674468_cae8894025_o.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/97/Consuegra_(Toledo)_(18329674468).jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Consuegra_(Toledo)_(18329674468).jpg/1280px-Consuegra_(Toledo)_(18329674468).jpg",
    ]),
    ("plaza-espana", [
        "https://upload.wikimedia.org/wikipedia/commons/6/64/Consuegra_(13910010000).jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Consuegra_(13910010000).jpg/1280px-Consuegra_(13910010000).jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Consuegra_(13910010000).jpg/960px-Consuegra_(13910010000).jpg",
    ]),
]

html = HTML.read_text(encoding="utf-8")
for slug, urls in PHOTOS:
    target = OUT / f"{slug}.webp"
    success = False
    for source in urls:
        for attempt in range(2):
            try:
                request = urllib.request.Request(source, headers={
                    "User-Agent": "Mozilla/5.0 (compatible; ElConsaburense/1.0)",
                    "Accept": "image/avif,image/webp,image/*,*/*;q=0.8",
                })
                with urllib.request.urlopen(request, timeout=14) as response:
                    raw = response.read(11_000_000)
                with Image.open(io.BytesIO(raw)) as original:
                    image = ImageOps.exif_transpose(original).convert("RGB")
                    image.thumbnail((1920, 1280), Image.Resampling.LANCZOS)
                    image.save(target, "WEBP", quality=87, method=5)
                if target.stat().st_size < 8_000:
                    raise ValueError("Fotografía incompleta")
                html = html.replace('src="' + urls[0] + '"',
                                    'src="media/consuegra/' + slug + '.webp"')
                print(f"MONUMENTO OK: {slug} ({target.stat().st_size} bytes)", flush=True)
                success = True
                break
            except Exception as error:
                print(f"FOTO {slug}: {str(error)[:120]}", flush=True)
                if attempt == 0:
                    time.sleep(0.8)
        if success:
            break
    if not success:
        target.unlink(missing_ok=True)
        # Conservamos en la página la foto original, sin inventar otro monumento.
        print(f"MONUMENTO EXTERNO: {slug}", flush=True)

HTML.write_text(html, encoding="utf-8")
