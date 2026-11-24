#!/usr/bin/env python3
"""make.fun entry for "Sum up 24 November's world news in one image".

The image beside this file, entry.png, is a one-page newspaper front
page of Tuesday 24 November 2026 (drawn by draw_image.py from the
story data in stories.py). This program copies it, byte for byte, to
/output/entry.png. It uses only the Python 3.13 standard library,
needs no network, and writes the same bytes on every run.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().with_name("entry.png")
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()
