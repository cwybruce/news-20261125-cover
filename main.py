#!/usr/bin/env python3
"""Entry for make.fun news-image-20261125.

Copies the pre-rendered cover image (entry.png, drawn by draw_cover.py)
into $MAKEFUN_OUTPUT_DIR/entry.png, byte-for-byte.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1 * 1024 * 1024  # competition cap: at most 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(SRC):
        print(f"error: source image missing: {SRC}", file=sys.stderr)
        sys.exit(1)
    with open(SRC, "rb") as fh:
        magic = fh.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        print("error: entry.png is not a PNG file", file=sys.stderr)
        sys.exit(1)
    src_size = os.path.getsize(SRC)
    if src_size > MAX_BYTES:
        print(f"error: entry.png is {src_size} bytes, over the "
              f"{MAX_BYTES}-byte cap", file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    dst_size = os.path.getsize(dst)
    if src_size != dst_size:
        print(f"error: incomplete copy ({dst_size} of {src_size} bytes)",
              file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print(f"wrote {dst} ({dst_size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
