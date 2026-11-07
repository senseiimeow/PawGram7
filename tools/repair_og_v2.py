#!/usr/bin/env python3
"""Properly restore og:image and og:url as two separate correct meta tags."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://senseiimeow.github.io/PawGram7"

# page path -> expected page URL segment
PAGE_PATHS = {
    "index.html": "index.html",
    "chapters.html": "chapters.html",
    "characters.html": "characters.html",
    "pawfun.html": "pawfun.html",
    "splash.html": "splash.html",
    "readers/Chapter_1_Reader.html": "readers/Chapter_1_Reader.html",
    "readers/Chapter_2_Reader.html": "readers/Chapter_2_Reader.html",
    "readers/Chapter_3_Reader.html": "readers/Chapter_3_Reader.html",
    "readers/Chapter_4_Reader.html": "readers/Chapter_4_Reader.html",
    "readers/Chapter_5_Reader.html": "readers/Chapter_5_Reader.html",
    "readers/Chapter_6_Reader.html": "readers/Chapter_6_Reader.html",
    "readers/Chapter_7_Reader.html": "readers/Chapter_7_Reader.html",
}

# The mangled line looks like:
#   <meta property="og:image" <meta property="og:url" content="SITE_URL/art/logo-512.png">
MANGLED = re.compile(
    r'<meta property="og:image" <meta property="og:url" content="%s/([^"]+)"\s*>' % SITE_URL
)

REPLACEMENT_TEMPLATE = (
    '<meta property="og:image" content="%s/art/logo-512.png">\n'
    '<meta property="og:url" content="%s/%s">'
)

def fix(rel, page_path):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    text2, n = MANGLED.subn(
        REPLACEMENT_TEMPLATE % (SITE_URL, SITE_URL, page_path),
        text,
        count=1,
    )
    if n:
        p.write_text(text2, encoding="utf-8")
        print("  (ok) %s: restored og:image + og:url" % rel)
    else:
        print("  (skip) %s: mangled pattern not found" % rel)

def main():
    for rel, page_path in PAGE_PATHS.items():
        fix(rel, page_path)

if __name__ == "__main__":
    main()
