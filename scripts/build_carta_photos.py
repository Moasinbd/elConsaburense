#!/usr/bin/env python3
"""Descarga fotos reales con licencia CC desde Wikimedia Commons y publica WebP locales.

Fail-closed: si una imagen no es válida, la publicación CI se detiene.
Las fotos representan platos similares; no son fotografías del restaurante.
"""
from __future__ import annotations

import io
import json
import urllib.parse
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
    {"slug": "croquetas", "source": "Croquetas jamón y cecina.jpg"},
    {"slug": "callos", "source": "Callos a la Madrileña.jpg"},
    {"slug": "entrecot", "source": "Entrecot de ternera.jpg"},
    {"slug": "arroz", "source": "Arroz con mariscos caldoso.jpg"},
    {"slug": "asado", "source": "Plato de lechazo, Valladolid.jpg"},
    {"slug": "tarta", "source": "Tarta de Queso.jpg"},
]
UA = "ElConsaburense-website/1.0 (food gallery; Wikimedia Commons attribution at elconsaburense.moasin.dev/creditos.html)"
HTTP_HEADERS = {"User-Agent": UA, "Accept": "image/jpeg,image/png,image/webp,image/*;q=0.8"}

def resolve_commons_urls(filename: str) -> list[str]:
    """Consulta MediaWiki para obtener las URLs reales (evita hashes de ruta inventados)."""
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "url", "iiurlwidth": "960", "titles": "File:" + filename
    })
    url = "https://commons.wikimedia.org/w/api.php?" + params
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        result = json.load(resp)
    pages = result.get("query", {}).get("pages", {})
    found = next((page["imageinfo"][0] for page in pages.values() if page.get("imageinfo")), None)
    if not found or not found.get("url"):
        raise ValueError(f"Commons sin imagen disponible: {filename}")
    return list(dict.fromkeys(x for x in (found.get("thumburl"), found["url"]) if x))

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
    try:
        addresses = resolve_commons_urls(item["source"])
    except (OSError, ValueError, urllib.error.URLError) as exc:
        sys.exit(f"No se ha podido identificar la foto {item['slug']}: {exc}")
    for address in addresses:
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
