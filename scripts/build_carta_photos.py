#!/usr/bin/env python3
"""Descarga fotos reales con licencia CC desde Wikimedia Commons y publica WebP locales.

Fail-closed: si una imagen no es válida, la publicación CI se detiene.
Las fotos representan platos similares; no son fotografías del restaurante.
"""
from __future__ import annotations

import io
import pathlib
import sys
import time
import urllib.error
import urllib.request

from PIL import Image, ImageOps, UnidentifiedImageError

BASE = pathlib.Path(__file__).resolve().parents[1]
OUT = BASE / "public" / "media" / "carta"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = [
  {
    "slug": "croquetas",
    "source": "Croquetas_jamón_y_cecina.jpg",
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Croquetas_jam%C3%B3n_y_cecina.jpg/960px-Croquetas_jam%C3%B3n_y_cecina.jpg",
    "original": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Croquetas_jam%C3%B3n_y_cecina.jpg"
  },
  {
    "slug": "callos",
    "source": "Callos_a_la_Madrileña.jpg",
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Callos_a_la_Madrile%C3%B1a.jpg/960px-Callos_a_la_Madrile%C3%B1a.jpg",
    "original": "https://upload.wikimedia.org/wikipedia/commons/d/dc/Callos_a_la_Madrile%C3%B1a.jpg"
  },
  {
    "slug": "entrecot",
    "source": "Entrecot_de_ternera.jpg",
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Entrecot_de_ternera.jpg/800px-Entrecot_de_ternera.jpg",
    "original": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Entrecot_de_ternera.jpg"
  },
  {
    "slug": "arroz",
    "source": "Arroz_caldoso_con_mariscos.jpg",
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Arroz_caldoso_con_mariscos.jpg/800px-Arroz_caldoso_con_mariscos.jpg",
    "original": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Arroz_caldoso_con_mariscos.jpg"
  },
  {
    "slug": "asado",
    "source": "Plato_de_lechazo,_Valladolid.jpg",
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Plato_de_lechazo%2C_Valladolid.jpg/800px-Plato_de_lechazo%2C_Valladolid.jpg",
    "original": "https://upload.wikimedia.org/wikipedia/commons/3/31/Plato_de_lechazo%2C_Valladolid.jpg"
  },
  {
    "slug": "tarta",
    "source": "Tarta_de_Queso.jpg",
    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Tarta_de_Queso.jpg/960px-Tarta_de_Queso.jpg",
    "original": "https://upload.wikimedia.org/wikipedia/commons/f/f7/Tarta_de_Queso.jpg"
  }
]
UA = "ElConsaburense-website/1.0 (food gallery; Wikimedia Commons attribution at elconsaburense.moasin.dev/creditos.html)"
HTTP_HEADERS = {"User-Agent": UA, "Accept": "image/jpeg,image/png,image/webp,image/*;q=0.8"}

def get_photo(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HTTP_HEADERS)
    with urllib.request.urlopen(request, timeout=28) as response:
        payload = response.read(9_000_000)
        if response.read(1):
            raise ValueError("Imagen excede el límite permitido")
    if len(payload) < 8000:
        raise ValueError(f"Imagen demasiado pequeña: {len(payload)} bytes")
    with Image.open(io.BytesIO(payload)) as image:
        image.verify()
    return payload

def save_webp(payload: bytes, destination: pathlib.Path) -> tuple[int,int,int]:
    with Image.open(io.BytesIO(payload)) as photo:
        if photo.width < 500 or photo.height < 400:
            raise ValueError(f"Resolución insuficiente: {photo.size}")
        photo = ImageOps.exif_transpose(photo).convert("RGB")
        # La copia adaptada se publica con su atribución y la misma licencia CC.
        photo = ImageOps.fit(photo, (960, 720), Image.Resampling.LANCZOS, centering=(0.5, 0.48))
        temporary = destination.with_suffix(".tmp.webp")
        photo.save(temporary, format="WEBP", quality=84, method=5)
    with Image.open(temporary) as verify:
        verify.verify()
    if temporary.stat().st_size < 10_000:
        raise ValueError("WebP demasiado pequeño")
    temporary.replace(destination)
    return 960, 720, destination.stat().st_size

for item in SOURCES:
    destination = OUT / (item["slug"] + ".webp")
    error = None
    for address in (item["thumbnail"], item["original"]):
        for attempt in range(1, 4):
            try:
                data = get_photo(address)
                w,h,weight = save_webp(data, destination)
                print(f"FOTO LOCAL OK {item['slug']} {w}x{h}, {weight} bytes", flush=True)
                error = None
                break
            except (OSError, ValueError, urllib.error.URLError, UnidentifiedImageError) as exc:
                error = str(exc)
                print(f"Reintento {item['slug']} {attempt}: {error[:120]}", flush=True)
                time.sleep(min(4, attempt * 1.2))
        if error is None:
            break
    if error is not None:
        sys.exit(f"No se publican imágenes rotas: {item['slug']} => {error}")
print("Seis fotografias locales verificadas y optimizadas", flush=True)
