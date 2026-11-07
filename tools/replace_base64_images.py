#!/usr/bin/env python3
"""Replace inline base64 WebP images in PawGram7 reader HTML files with
references to the actual WebP files in pages/chX/pYY.webp.

Preserves all other img attributes (alt, width, height, loading, decoding).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Chapter reader -> (chapter folder, number of pages)
CHAPTERS = {
    "readers/Chapter_1_Reader.html": ("ch1", 10),
    "readers/Chapter_2_Reader.html": ("ch2", 9),
    "readers/Chapter_3_Reader.html": ("ch3", 10),
    "readers/Chapter_4_Reader.html": ("ch4", 10),
    "readers/Chapter_5_Reader.html": ("ch5", 10),
    "readers/Chapter_6_Reader.html": ("ch6", 10),
    "readers/Chapter_7_Reader.html": ("ch7", 10),
}

# Match: <img src="data:image/webp;base64,<long base64>" [other attrs...]>
# base64 alphabet: A-Za-z0-9+/= — no double quotes, so we can match to the next "
IMG_RE = re.compile(
    r'<img\s+src="data:image/webp;base64,[A-Za-z0-9+/=]*"',
    re.DOTALL,
)

def process(rel, chapter, total_pages):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")

    matches = list(IMG_RE.finditer(text))
    found = len(matches)
    print(f"  {rel}: found {found} base64 images (expecting {total_pages})")

    if found != total_pages:
        print(f"    !! WARNING: count mismatch, skipping {rel}")
        return 0

    # Replace each match sequentially with pages/chX/pYY.webp
    parts = []
    last_end = 0
    replaced = 0
    for idx, m in enumerate(matches, start=1):
        new_src = f'pages/{chapter}/p{idx:02d}.webp'
        parts.append(text[last_end:m.start()])
        parts.append(f'<img src="{new_src}"')
        last_end = m.end()
        replaced += 1
    parts.append(text[last_end:])

    p.write_text("".join(parts), encoding="utf-8")
    print(f"    -> replaced {replaced} images with file paths")
    return replaced

def main():
    total = 0
    for rel, (chapter, n_pages) in CHAPTERS.items():
        total += process(rel, chapter, n_pages)
    print(f"\nTotal images replaced: {total}")

if __name__ == "__main__":
    main()
