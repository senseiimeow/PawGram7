#!/usr/bin/env python3
"""Add Open Graph / Twitter Card meta tags to all PawGram7 HTML pages,
create sitemap.xml + robots.txt, and clean up sw.js precache list."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per-page SEO data (relative path -> title override, description override, image)
PAGES = {
    "index.html": {
        "title": "PAWGRAM — See You Offline · Season 1",
        "desc": "PAWGRAM — SEE YOU OFFLINE, a full-color manhwa about two strangers, seven months of messages, and one day under the sakura.",
        "image": "art/logo-512.png",
        "type": "website",
    },
    "chapters.html": {
        "title": "Chapters — PAWGRAM · See You Offline",
        "desc": "All 7 chapters of PAWGRAM — SEE YOU OFFLINE. Palettes, loglines and where to start reading.",
        "image": "art/logo-512.png",
        "type": "website",
    },
    "characters.html": {
        "title": "Cast — PAWGRAM · See You Offline",
        "desc": "Meet Tejas, Pragati, Mochi and the Midnight Strays — the character bible of PAWGRAM.",
        "image": "art/logo-512.png",
        "type": "website",
    },
    "pawfun.html": {
        "title": "PawFun — PAWGRAM · See You Offline",
        "desc": "PawFun arcade — 4 mini-games: Paw Catch, Konbini Rush, Thread Quiz, Umbrella Dash.",
        "image": "art/logo-512.png",
        "type": "website",
    },
    "splash.html": {
        "title": "PAWGRAM",
        "desc": "PAWGRAM — SEE YOU OFFLINE. Loading into the story.",
        "image": "art/logo-512.png",
        "type": "website",
    },
}

READERS = {
    "readers/Chapter_1_Reader.html": "Chapter 1 · Low Battery",
    "readers/Chapter_2_Reader.html": "Chapter 2 · New Member",
    "readers/Chapter_3_Reader.html": "Chapter 3 · Direct Message",
    "readers/Chapter_4_Reader.html": "Chapter 4 · Two Months of Midnight",
    "readers/Chapter_5_Reader.html": "Chapter 5 · Winter, Held Together",
    "readers/Chapter_6_Reader.html": "Chapter 6 · Counting Down to Spring",
    "readers/Chapter_7_Reader.html": "Chapter 7 · See You Offline",
}

# Use GitHub Pages URL as default; replace with your real domain if deployed elsewhere.
SITE_URL = "https://senseiimeow.github.io/PawGram7"

OG_TEMPLATE = '''<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{otype}">
<meta property="og:image" content="{url}/{image}">
<meta property="og:image:alt" content="{title}">
<meta property="og:url" content="{url}/{path}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{url}/{image}">'''


def add_og_tags(path: Path, data: dict):
    text = path.read_text(encoding="utf-8")
    if 'property="og:title"' in text:
        print(f"  (skip) {path}: OG tags already present")
        return
    og = OG_TEMPLATE.format(
        title=data["title"],
        desc=data["desc"],
        otype=data["type"],
        image=data["image"],
        url=SITE_URL,
        path=path.as_posix(),
    )
    # Insert right after the description meta tag line
    pattern = re.compile(r'(<meta name="description" content="[^"]*">\n)')
    m = pattern.search(text)
    if not m:
        print(f"  (warn) {path}: no description meta found, inserting after <title>")
        text = text.replace('</title>', '</title>\n' + og, 1)
    else:
        text = text[: m.end()] + og + "\n" + text[m.end() :]
    path.write_text(text, encoding="utf-8")
    print(f"  (ok) {path}: OG/Twitter tags added")


def main():
    print("== Adding OG/Twitter tags ==")
    for rel, data in PAGES.items():
        add_og_tags(ROOT / rel, data)
    for rel, chapter_title in READERS.items():
        add_og_tags(
            ROOT / rel,
            {
                "title": f"{chapter_title} — PAWGRAM · See You Offline",
                "desc": f"Read {chapter_title} — Chapter of PAWGRAM, a full-color manhwa about two strangers, seven months of messages, and one day under the sakura.",
                "image": "art/logo-512.png",
                "type": "website",
            },
        )

    print("\n== Creating sitemap.xml ==")
    urls = []
    for rel in list(PAGES) + list(READERS):
        urls.append(f"  <url><loc>{SITE_URL}/{rel}</loc></url>")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  (ok) sitemap.xml with {len(urls)} urls")

    print("\n== Creating robots.txt ==")
    robots = "User-agent: *\nAllow: /\nSitemap: {}/sitemap.xml\n".format(SITE_URL)
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print("  (ok) robots.txt")

    print("\n== Fixing sw.js precache list ==")
    sw = ROOT / "sw.js"
    text = sw.read_text(encoding="utf-8")
    # Remove references to non-existent _src files from the CORE precache list
    cleaned = re.sub(r"\s*'./_src/[^']+',\n?", "", text)
    sw.write_text(cleaned, encoding="utf-8")
    print("  (ok) sw.js: removed missing ./_src/* entries")


if __name__ == "__main__":
    main()
