#!/usr/bin/env python3
"""Genera el vídeo de 15 s desde recursos locales; no descarga fotos en CI."""
from __future__ import annotations

import pathlib
import subprocess
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
MEDIA = ROOT / "public" / "media"
MEDIA.mkdir(parents=True, exist_ok=True)

# build_town_gallery.py se ejecuta antes y prepara estos recursos locales.
SCENES = [
    ("molinos", MEDIA / "consuegra" / "molinos.webp"),
    ("castillo", MEDIA / "consuegra" / "castillo.webp"),
    ("croquetas", MEDIA / "platos" / "croquetas-tapas.webp"),
    ("bravas", MEDIA / "platos" / "patatas-bravas.webp"),
    ("ensaladilla", MEDIA / "platos" / "ensaladilla-rusa.webp"),
]
WIDTH, HEIGHT, FPS = 960, 540, 24
CLIP_SECONDS = 3
OUTPUT = MEDIA / "consaburense-15s.mp4"

def read_scene(source: pathlib.Path) -> Image.Image:
    if not source.is_file():
        raise FileNotFoundError(f"Fotografía local no disponible: {source}")
    with Image.open(source) as image:
        return image.convert("RGB")

def generate_video() -> None:
    frames: list[pathlib.Path] = []
    try:
        for index, (name, source) in enumerate(SCENES):
            image = read_scene(source)
            image = ImageOps.fit(
                image, (WIDTH, HEIGHT),
                method=Image.Resampling.LANCZOS, centering=(0.5, 0.48)
            )
            frame = MEDIA / f"_video-frame-{index}.jpg"
            image.save(frame, "JPEG", quality=88, optimize=True)
            frames.append(frame)
            print(f"Fotograma local: {name}", flush=True)

        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
        for frame in frames:
            cmd += ["-loop", "1", "-framerate", str(FPS), "-t",
                    str(CLIP_SECONDS), "-i", str(frame)]
        filters = [
            f"[{i}:v]scale={WIDTH}:{HEIGHT},setsar=1,fps={FPS},"
            f"format=yuv420p,trim=duration={CLIP_SECONDS},setpts=PTS-STARTPTS[v{i}]"
            for i in range(len(frames))
        ]
        inputs = "".join(f"[v{i}]" for i in range(len(frames)))
        filters.append(
            f"{inputs}concat=n={len(frames)}:v=1:a=0,format=yuv420p[video]"
        )
        cmd += [
            "-filter_complex", ";".join(filters), "-map", "[video]",
            "-t", "15", "-an", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "24", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-r", str(FPS), str(OUTPUT)
        ]
        subprocess.run(cmd, check=True)
        if OUTPUT.stat().st_size < 10_000:
            raise RuntimeError("Vídeo generado vacío")
        print(f"Vídeo de 15 s desde fotografías locales: {OUTPUT.stat().st_size} bytes")
    finally:
        for frame in frames:
            frame.unlink(missing_ok=True)

if __name__ == "__main__":
    generate_video()
