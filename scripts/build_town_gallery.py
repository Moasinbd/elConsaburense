#!/usr/bin/env python3
"""Optimiza fotografías reales de Consuegra y evita dependencias externas si se descargan."""
from __future__ import annotations

import io
import json
import pathlib
import re
import time
import urllib.parse
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

# URLs de los fotógrafos originales (o alternativa Creative Commons si la foto
# del castillo de Wikimedia no puede descargarse).
FLICKR_PHOTOS = {
    "molinos": "https://www.flickr.com/photos/alvaromoreno/52322755265/",
    "castillo": "https://www.flickr.com/photos/kentwang/49946328342/",
    "plaza-espana": "https://www.flickr.com/photos/martius/13910010000/",
}

def flickr_image_candidates(slug: str) -> list[str]:
    """Resuelve URL de imagen mediante oEmbed público, sin claves privadas."""
    page = FLICKR_PHOTOS.get(slug)
    if not page:
        return []
    options = {
        "url": page,
        "format": "json",
        "maxwidth": "1280",
        "maxheight": "960",
    }
    api = "https://www.flickr.com/services/oembed/?" + urllib.parse.urlencode(options)
    try:
        request = urllib.request.Request(api, headers={
            "User-Agent": "Mozilla/5.0 (compatible; ElConsaburense/1.0)",
            "Accept": "application/json,*/*;q=0.8",
        })
        with urllib.request.urlopen(request, timeout=12) as response:
            details = json.load(response)
        urls = [
            details.get("url"),
            details.get("thumbnail_url"),
        ]
        urls = [link for link in urls if isinstance(link, str)
                and link.startswith(("https://live.staticflickr.com/",
                                     "https://farm",
                                     "http://farm"))]
        # Reutiliza la imagen de 1024 px si el oEmbed devuelve una miniatura.
        for link in urls[:]:
            large = re.sub(r"_[sqtmnzwo]\.jpg$", "_b.jpg", link)
            if large != link:
                urls.insert(0, large.replace("http://", "https://"))
        unique = list(dict.fromkeys(u.replace("http://", "https://") for u in urls))
        print(f"FLICKR OEmbed: {slug} ({len(unique)} tamaños)", flush=True)
        return unique
    except Exception as error:
        print(f"FLICKR OEmbed falla {slug}: {str(error)[:140]}", flush=True)
        return []

html = HTML.read_text(encoding="utf-8")
for slug, urls in PHOTOS:
    source_options = flickr_image_candidates(slug) + urls
    target = OUT / f"{slug}.webp"
    success = False
    for source in source_options:
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
