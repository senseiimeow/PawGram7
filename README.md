# PAWGRAM — SEE YOU OFFLINE · Season 1

A full-colour manhwa site: 7 chapters, 69 pages, one story that goes from a 2:47 AM
group chat to an afternoon under the sakura.

## What's in this folder

| Path | What it is |
|---|---|
| `index.html` | Home — hero, story, cast, chapters rail, motifs, gallery |
| `chapters.html` | All 7 chapters with palettes and loglines |
| `characters.html` | Character bible: Tejas, Pragati, Mochi, the Midnight Strays |
| `pawfun.html` | **PawFun arcade** — 4 mini-games (Paw Catch, Konbini Rush, Thread Quiz, Umbrella Dash) |
| `pawfun.html` | All 4 mini-games + arcade styles inline (vanilla JS, no dependencies) |
| `readers/Chapter_1..7_Reader.html` | The actual chapters, 69 illustrated pages |
| `pages/` | Page art as WebP (43–90 KB each) |
| `art/` + `art/thumb/` | Cast portraits, gallery art and 560px thumbnails |
| `manifest.webmanifest`, `sw.js`, `splash.html` | Makes it installable + offline-readable (PWA) |

## Run it anywhere

It is a **static site** — no backend, no build step needed at runtime. Any of these work:

```bash
# local
python3 -m http.server 8000        # then open http://localhost:8000

# or drop the whole folder on any static host
# Netlify / Vercel / Cloudflare Pages / GitHub Pages / Neocities — just upload the folder
```

## Self-contained pages
Every page inlines its own CSS, JavaScript and art (as data URIs), so a page renders fully
even when it is opened in a sandboxed iframe or with no network at all. That is why the
arcade and the readers work inside in-app previews as well as on a real host.

## Publishing checklist
- [x] All paths are **relative** (works in a subfolder or at a domain root)
- [x] No external CDNs, fonts or trackers — everything is self-contained
- [x] Total weight 7.8 MB for the whole site; ~97 KB for a first paint
- [x] Installable on Android/iOS via the PWA manifest
- [x] Service worker caches art so chapters read offline after the first visit

## Credits
Story, script, character locks and page direction: the SEE YOU OFFLINE production bible.
Site design and build: PAWGRAM.
