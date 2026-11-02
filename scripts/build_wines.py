#!/usr/bin/env python3
"""Optimiza fotos de ambientación vinícola; nunca simula etiquetas auténticas."""
from __future__ import annotations

import io
import pathlib
import time
import urllib.request
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "media" / "vinos"
HTML_PATH = ROOT / "public" / "index.html"
OUT.mkdir(parents=True, exist_ok=True)
PHOTOS = [
    ("calderico", "8473209"),
    ("castillo-consuegra", "28304430"),
    ("altovela", "8473221"),
    ("ojos-guadiana", "8088400"),
    ("alcardet", "10508457"),
    ("finca-antigua", "4110399"),
]
html = HTML_PATH.read_text(encoding="utf-8")
for slug, photo_id in PHOTOS:
    url = (f"https://images.pexels.com/photos/{photo_id}/"
           f"pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=1280")
    target = OUT / f"{slug}.webp"
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; ElConsaburense/1.0)",
                "Accept": "image/*,*/*;q=0.8",
            })
            with urllib.request.urlopen(request, timeout=18) as response:
                data = response.read(12_000_000)
            with Image.open(io.BytesIO(data)) as image:
                photo = ImageOps.fit(
                    image.convert("RGB"), (900, 750),
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.46),
                )
            photo.save(target, "WEBP", quality=84, method=5)
            if target.stat().st_size < 5000:
                raise ValueError("Imagen demasiado pequeña")
            html = html.replace('src="' + url.replace('&', '&amp;') + '"',
                                f'src="media/vinos/{slug}.webp"')
            print(f"VINO FOTO OK: {slug}", flush=True)
            break
        except Exception as error:
            print(f"Descarga fallida {slug}: {error}", flush=True)
            if attempt < 2:
                time.sleep(1 + attempt)
    else:
        print(f"VINO FOTO EXTERNA: {slug}", flush=True)
HTML_PATH.write_text(html, encoding="utf-8")
