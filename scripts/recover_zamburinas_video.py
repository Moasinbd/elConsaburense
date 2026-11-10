#!/usr/bin/env python3
"""Recover the original promotional video for El Consaburense.

The eight Base64 source parts preserve the video exactly. They are
transport encoding, not encryption. Output integrity is SHA256 checked.
"""
from __future__ import annotations

import base64
import hashlib
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = ROOT / "assets" / "zamburinas-promo"
TARGET = ROOT / "public" / "media" / "zamburinas-huevo-patatas-consaburense.mp4"
SHA256 = "b8809a55594dd26d1be6fcab73b32295ab5145d7dc5aa260d7943aa878bcc234"


def main() -> None:
    parts = sorted(SOURCES.glob("part-*.b64"))
    expected = [f"part-{index:02d}.b64" for index in range(1, 9)]
    if [part.name for part in parts] != expected:
        raise RuntimeError("Missing or misnumbered promotional video parts")
    encoded = "".join("".join(part.read_text(encoding="ascii").split()) for part in parts)
    content = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(content).hexdigest()
    if actual != SHA256:
        raise RuntimeError(f"Video integrity error: {actual}")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(content)
    subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
                    "-of", "default=noprint_wrappers=1", str(TARGET)], check=True)
    print(f"Verified promotional video: {TARGET.relative_to(ROOT)} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
