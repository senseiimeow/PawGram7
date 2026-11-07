#!/usr/bin/env python3
"""Repair the broken og:url lines: '<meta property=...> content=...' lost its prefix."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://senseiimeow.github.io/PawGram7"

FILES = [
    "index.html", "chapters.html", "characters.html", "pawfun.html", "splash.html",
    "readers/Chapter_1_Reader.html", "readers/Chapter_2_Reader.html",
    "readers/Chapter_3_Reader.html", "readers/Chapter_4_Reader.html",
    "readers/Chapter_5_Reader.html", "readers/Chapter_6_Reader.html",
    "readers/Chapter_7_Reader.html",
]

PATTERN = re.compile(r'content="%s/([^"]+)"\s*>' % SITE_URL)

def fix(rel):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    m = PATTERN.search(text)
    if not m:
        print("  (skip) %s: no broken og:url line found" % rel)
        return
    # Replace the bare content=...> line with a proper meta tag
    text2, n = PATTERN.subn(
        '<meta property="og:url" content="%s/%s">' % (SITE_URL, m.group(1)),
        text,
        count=1,
    )
    p.write_text(text2, encoding="utf-8")
    print("  (ok) %s: repaired og:url -> %s" % (rel, m.group(1)))

def main():
    for rel in FILES:
        fix(rel)

if __name__ == "__main__":
    main()
