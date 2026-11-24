#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with a read-only repository, so the program
must never write next to itself: the only output is
os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png
"""
import hashlib
import os
import shutil
import struct
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    w, h = png_size(dst)
    if (w, h) != (1024, 1024):
        raise SystemExit(f"bad size {w}x{h}, expected 1024x1024")
    if sha256(src) != sha256(dst):
        raise SystemExit("sha256 mismatch between entry.png and output")
    size = os.path.getsize(dst)
    if size > 1048576:
        raise SystemExit(f"entry.png too large: {size} bytes")
    print(f"OK entry.png {w}x{h} {size} bytes sha256={sha256(dst)[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
