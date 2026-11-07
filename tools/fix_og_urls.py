#!/usr/bin/env python3
"""Fix og:url to use relative paths, add description meta to pages missing it,
and remove the dead _src/ stylesheet link from splash.html."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://senseiimeow.github.io/PawGram7"

DESCRIPTIONS = {
    "index.html": "PAWGRAM — SEE YOU OFFLINE, a full-color manhwa about two strangers, seven months of messages, and one day under the sakura.",
    "chapters.html": "All 7 chapters of PAWGRAM — SEE YOU OFFLINE. Palettes, loglines and where to start reading.",
    "characters.html": "Meet Tejas, Pragati, Mochi and the Midnight Strays — the character bible of PAWGRAM.",
    "pawfun.html": "PawFun arcade — 4 mini-games: Paw Catch, Konbini Rush, Thread Quiz, Umbrella Dash.",
    "splash.html": "PAWGRAM — SEE YOU OFFLINE. Loading into the story.",
    "readers/Chapter_1_Reader.html": "Chapter 1 · Low Battery — Read the opening chapter of PAWGRAM, a full-color manhwa about two strangers, seven months of messages, and one day under the sakura.",
    "readers/Chapter_2_Reader.html": "Chapter 2 · New Member — Tejas and Pragati take the next step after seven months of midnight messages.",
    "readers/Chapter_3_Reader.html": "Chapter 3 · Direct Message — Words that cross the screen and land in the heart.",
    "readers/Chapter_4_Reader.html": "Chapter 4 · Two Months of Midnight — The countdown to spring begins.",
    "readers/Chapter_5_Reader.html": "Chapter 5 · Winter, Held Together — Two strangers learning how to share a season.",
    "readers/Chapter_6_Reader.html": "Chapter 6 · Counting Down to Spring — Almost there. Almost together.",
    "readers/Chapter_7_Reader.html": "Chapter 7 · See You Offline — The meeting under the sakura.",
}

def fix_file(rel: str, desc: str):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    changed = []

    # 1) Fix og:url: replace wrong absolute-filesystem path with relative path
    def repl_url(m):
        changed.append("og:url fixed")
        return 'content="%s/%s"' % (SITE_URL, rel)

    text, n = re.subn(
        r'<meta property="og:url" content="[^"]*"',
        repl_url,
        text,
        count=1,
    )

    # 2) Add description meta if missing (insert after </title>)
    if desc and 'name="description"' not in text:
        text = text.replace('</title>', '</title>\n<meta name="description" content="%s">' % desc, 1)
        changed.append("description meta added")

    # 3) splash.html: drop dead stylesheet link to missing _src/site.css
    if rel == "splash.html":
        text2, n2 = re.subn(
            r'<link rel="stylesheet" href="_src/site\.css\?v=2\.1">\n?',
            "",
            text,
        )
        if n2:
            text = text2
            changed.append("dead _src stylesheet removed")

    if changed:
        p.write_text(text, encoding="utf-8")
        print("  (ok) %s: %s" % (rel, ", ".join(changed)))
    else:
        print("  (skip) %s: no changes needed" % rel)

def main():
    for rel, desc in DESCRIPTIONS.items():
        fix_file(rel, desc)

if __name__ == "__main__":
    main()
