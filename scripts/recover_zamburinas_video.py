#!/usr/bin/env python3
"""Build the preparation-only portrait video from the verified 30s source.

The original promotional video includes still-photo intros/outros. Keep only
the chef footage: 4.00s through 23.45s, preserving the music and corner logo.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "zamburinas-30s"
DEST = ROOT / "public" / "media"
SOURCE_SHA256 = "b38a11991eada2351be768c183517bb25b376bf3329b0aab7ff5a3156deac5e8"
SOURCE_SIZE = 2896030
OUTPUT = DEST / "zamburinas-preparacion-sin-fotos-v2.mp4"
POSTER = DEST / "zamburinas-preparacion-cartel-v2.webp"


def execute(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    parts = sorted(SOURCE.glob("part-*.bin"))
    expected = [f"part-{i:02d}.bin" for i in range(1, 17)]
    if [p.name for p in parts] != expected:
        raise RuntimeError("Missing source video parts")
    data = b"".join(p.read_bytes() for p in parts)
    if len(data) != SOURCE_SIZE or hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise RuntimeError("Invalid 30-second source video checksum")

    DEST.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        original = pathlib.Path(tmp) / "verified-original.mp4"
        original.write_bytes(data)
        execute(
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", "4.0", "-i", str(original), "-t", "19.45",
            "-map", "0:v:0", "-map", "0:a:0",
            "-vf", "fps=30,format=yuv420p",
            "-af", "afade=t=in:st=0:d=0.18,afade=t=out:st=19.10:d=0.35",
            "-c:v", "libx264", "-preset", "medium", "-crf", "22",
            "-c:a", "aac", "-b:a", "112k", "-movflags", "+faststart",
            str(OUTPUT),
        )

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "format=duration:stream=width,height",
         "-of", "json", str(OUTPUT)],
        check=True, capture_output=True, text=True,
    )
    meta = json.loads(probe.stdout)
    video = meta["streams"][0]
    duration = float(meta["format"]["duration"])
    if (video["width"], video["height"]) != (540, 960) or not 19.2 < duration < 19.7:
        raise RuntimeError(f"Unexpected preparation video: {meta}")
    execute(
        "ffmpeg", "-y", "-loglevel", "error", "-ss", "11", "-i", str(OUTPUT),
        "-frames:v", "1", "-vf", "scale=540:960",
        "-c:v", "libwebp", "-q:v", "78", str(POSTER),
    )
    if POSTER.stat().st_size < 1000:
        raise RuntimeError("Failed to generate preparation-only poster")

    # Avoid retaining the old intro/outro at the two published legacy paths.
    for old_name in ("zamburinas-30s-20261110.mp4",
                     "zamburinas-huevo-patatas-consaburense.mp4"):
        shutil.copyfile(OUTPUT, DEST / old_name)
    shutil.copyfile(POSTER, DEST / "zamburinas-cartel-20261110.webp")
    print(f"Validated preparation-only cut: {duration:.2f}s at 540x960 ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
