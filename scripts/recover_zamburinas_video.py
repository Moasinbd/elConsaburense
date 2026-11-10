#!/usr/bin/env python3
"""Rebuild the exact 30-second vertical corporate video from 16 binary parts."""
from __future__ import annotations
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "zamburinas-30s"
DEST = ROOT / "public" / "media"
SHA256 = "b38a11991eada2351be768c183517bb25b376bf3329b0aab7ff5a3156deac5e8"
SIZE = 2896030

def main():
    paths = sorted(SOURCE.glob("part-*.bin"))
    expected = [f"part-{i:02d}.bin" for i in range(1, 17)]
    if [p.name for p in paths] != expected:
        raise RuntimeError("Missing video parts")
    data = b"".join(p.read_bytes() for p in paths)
    if len(data) != SIZE or hashlib.sha256(data).hexdigest() != SHA256:
        raise RuntimeError("Invalid video checksum")
    DEST.mkdir(parents=True, exist_ok=True)
    mp4 = DEST / "zamburinas-30s-20261110.mp4"
    mp4.write_bytes(data)
    (DEST / "zamburinas-huevo-patatas-consaburense.mp4").write_bytes(data)
    info = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","format=duration:stream=width,height","-of","json",str(mp4)],capture_output=True,text=True,check=True)
    meta=json.loads(info.stdout)
    video=meta["streams"][0]
    if video["width"]!=540 or video["height"]!=960 or abs(float(meta["format"]["duration"])-30)>0.2:
        raise RuntimeError("Unexpected video dimensions or duration")
    poster=DEST / "zamburinas-cartel-20261110.webp"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","0.9","-i",str(mp4),"-frames:v","1","-vf","scale=540:960","-c:v","libwebp","-q:v","78",str(poster)],check=True)
    if poster.stat().st_size<1000:raise RuntimeError("Poster generation failed")
    print("Verified promotional video",mp4,"seconds:",meta["format"]["duration"])

if __name__=="__main__":
    main()
