#!/usr/bin/env python3
"""Crea el vídeo de portada: 15 segundos SIN nombres, rótulos ni logotipos."""
from __future__ import annotations

import io
import pathlib
import subprocess
import time
import urllib.request
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
MEDIA = ROOT / "public" / "media"
MEDIA.mkdir(parents=True, exist_ok=True)

# Los tres últimos fotogramas usan las fotografías locales de la carta.
SCENES = [
    ("molinos", "https://upload.wikimedia.org/wikipedia/commons/e/e0/"
     "Windmills_and_castle_of_Consuegra_%287079301421%29.jpg"),
    ("castillo", "https://upload.wikimedia.org/wikipedia/commons/9/9d/"
     "Castillo_de_Consuegra.jpg"),
    ("croquetas", MEDIA / "platos" / "croquetas-tapas.webp"),
    ("bravas", MEDIA / "platos" / "patatas-bravas.webp"),
    ("ensaladilla", MEDIA / "platos" / "ensaladilla-rusa.webp"),
]

WIDTH, HEIGHT, FPS = 960, 540, 24
CLIP_SECONDS = 3
OUTPUT = MEDIA / "consaburense-15s.mp4"

def read_scene(source: str | pathlib.Path) -> Image.Image:
    """Carga una foto, utilizando otra foto local si falla Wikimedia Commons."""
    if isinstance(source, pathlib.Path):
        with Image.open(source) as image:
            return image.convert("RGB")
    for attempt in range(3):
        try:
            request = urllib.request.Request(source, headers={
                "User-Agent": "Mozilla/5.0 (compatible; ElConsaburense/1.0)",
                "Accept": "image/*,*/*;q=0.8",
            })
            with urllib.request.urlopen(request, timeout=18) as response:
                data = response.read(15_000_000)
            with Image.open(io.BytesIO(data)) as image:
                return image.convert("RGB")
        except Exception as error:
            print(f"Error fotográfico {attempt + 1}/3: {error}", flush=True)
            if attempt < 2:
                time.sleep(1 + attempt)
    fallback = MEDIA / "platos" / "tortilla-patatas.webp"
    if not fallback.is_file():
        raise RuntimeError("No hay imágenes disponibles para crear el vídeo")
    with Image.open(fallback) as image:
        return image.convert("RGB")

def generate_video() -> None:
    frames: list[pathlib.Path] = []
    try:
        for index, (name, source) in enumerate(SCENES):
            image = read_scene(source)
            # Exclusivamente imagen. Sin ImageDraw, letras ni logotipo superpuesto.
            image = ImageOps.fit(image, (WIDTH, HEIGHT),
                                 method=Image.Resampling.LANCZOS,
                                 centering=(0.5, 0.48))
            frame = MEDIA / f"_video-frame-{index}.jpg"
            image.save(frame, "JPEG", quality=88, optimize=True)
            frames.append(frame)
            print(f"Fotograma listo: {name}", flush=True)

        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
        for frame in frames:
            cmd += ["-loop", "1", "-framerate", str(FPS), "-t",
                    str(CLIP_SECONDS), "-i", str(frame)]
        filters = [
            f"[{i}:v]scale={WIDTH}:{HEIGHT},setsar=1,fps={FPS},"
            f"format=yuv420p,trim=duration={CLIP_SECONDS},"
            f"setpts=PTS-STARTPTS[v{i}]"
            for i in range(len(frames))
        ]
        inputs = "".join(f"[v{i}]" for i in range(len(frames)))
        filters.append(
            f"{inputs}concat=n={len(frames)}:v=1:a=0,"
            "format=yuv420p[video]"
        )
        cmd += ["-filter_complex", ";".join(filters), "-map", "[video]",
                "-t", "15", "-an", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-r", str(FPS), str(OUTPUT)]
        subprocess.run(cmd, check=True)
        if OUTPUT.stat().st_size < 10_000:
            raise RuntimeError("El MP4 generado está vacío")
        print(f"VÍDEO SIN TEXTOS GENERADO: {OUTPUT}", flush=True)
    finally:
        for frame in frames:
            frame.unlink(missing_ok=True)

if __name__ == "__main__":
    generate_video()
