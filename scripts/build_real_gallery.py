#!/usr/bin/env python3
"""Publica únicamente fotografías auténticas autorizadas que existan en el repo.

No descarga fotos ni genera imágenes. Si no hay fotos, la sección permanece ausente.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
INDEX = PUBLIC / "index.html"
PHOTOS = PUBLIC / "media" / "fotos-reales"
MANIFEST = PHOTOS / "manifest.json"
START = "<!-- REAL_RESTAURANT_GALLERY_START -->"
END = "<!-- REAL_RESTAURANT_GALLERY_END -->"

def main() -> None:
    page = INDEX.read_text(encoding="utf-8")
    if page.count(START) != 1 or page.count(END) != 1:
        raise RuntimeError("Faltan marcadores de la galería real")
    before, remaining = page.split(START, 1)
    _, after = remaining.split(END, 1)
    config = json.loads(MANIFEST.read_text(encoding="utf-8"))
    photos = config.get("photos", [])
    if not isinstance(photos, list) or len(photos) > 12:
        raise ValueError("El manifiesto de fotos debe ser una lista de hasta 12 elementos")
    cards = []
    seen = set()
    for entry in photos:
        if not isinstance(entry, dict):
            raise ValueError("Cada foto debe ser un objeto")
        name = entry.get("file")
        if not isinstance(name, str) or not name.endswith((".webp", ".jpg", ".jpeg", ".png")):
            raise ValueError("Nombre/extensión de fotografía no permitida")
        # Solo archivos propios de este directorio: nunca rutas relativas o remotas.
        if Path(name).name != name or name in seen:
            raise ValueError("Ruta o fotografía duplicada")
        seen.add(name)
        source = PHOTOS / name
        if not source.is_file() or source.stat().st_size < 1000:
            raise FileNotFoundError(f"Fotografía autorizada inexistente: {name}")
        title, description, credit = (
            entry.get("title"), entry.get("alt"), entry.get("credit")
        )
        if not all(isinstance(x, str) and 5 <= len(x.strip()) <= 160 for x in (title, description, credit)):
            raise ValueError("Cada foto necesita título, texto alternativo y crédito")
        clean = lambda s: html.escape(s.strip(), quote=True)
        cards.append(
            '        <figure>'
            f'<img src="media/fotos-reales/{clean(name)}" alt="{clean(description)}" '
            'width="960" height="720" loading="lazy" decoding="async">'
            f'<figcaption>{clean(title)}<small>Foto: {clean(credit)}</small></figcaption>'
            '</figure>'
        )
    block = ""
    if cards:
        block = (
            '\n    <section class="section real-gallery-section" id="fotos-reales" '
            'aria-labelledby="real-gallery-title">\n'
            '      <div class="wrap"><div class="real-gallery-intro">'
            '<span class="eyebrow">EL RESTAURANTE DE VERDAD</span>'
            '<h2 id="real-gallery-title">Así se vive El Consaburense</h2>'
            '<p>Fotografías reales aportadas y autorizadas por el establecimiento.</p>'
            '</div><div class="real-gallery-grid">\n'
            + '\n'.join(cards) + '\n</div></div></section>\n    '
        )
    INDEX.write_text(before + START + block + END + after, encoding="utf-8")
    print(f"Fotos auténticas publicadas: {len(cards)}")

if __name__ == "__main__":
    main()
