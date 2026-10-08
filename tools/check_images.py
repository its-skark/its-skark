#!/usr/bin/env python3
"""
Verify every image in README.md resolves to a REAL rendered value.

HTTP 200 is not enough: shields.io answers 200 with "badge not found" baked into
the SVG, and third-party cards can answer 200 with an empty document. This
checker inspects the response body so a broken badge fails the check.

Usage:  python3 tools/check_images.py
"""
from __future__ import annotations

import html as htmllib
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (compatible; readme-image-check/1.0)"}

# Phrases that only ever appear in a *failed* badge. Bare "404" must NOT be
# matched: it is a legitimate hex colour (e.g. Express 404040) and shows up in
# the generated SVG as a fill value, not as an error message.
BAD_PATTERNS = re.compile(
    r"badge not found|invalid\s+(color|value|query)|unable to (fetch|resolve)|"
    r"error:\s|repo not found|user not found|rate limit",
    re.I,
)


def strip_comments(text: str) -> str:
    """HTML comments never render, so nothing inside them is a real image."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def images() -> list[tuple[str, str]]:
    text = strip_comments((ROOT / "README.md").read_text(encoding="utf-8"))
    out: list[tuple[str, str]] = []
    for m in re.finditer(r'<img\b[^>]*src="([^"]+)"[^>]*>', text):
        src = htmllib.unescape(m.group(1))
        if src.startswith("data:"):
            out.append(("SKIP", src[:40]))
            continue
        # A `?v=` suffix is a cache-busting query, not part of the file name.
        is_local = not src.startswith("http")
        path = src.split("?", 1)[0] if is_local else src
        out.append((("REL:" + path) if is_local else src, path))
    return out


def probe(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read(400_000).decode("utf-8", "replace")
            return r.status, body
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:                                  # noqa: BLE001
        return -1, str(e)[:120]


def main() -> int:
    fails = 0
    seen: set[str] = set()
    for kind, url in images():
        if url in seen:
            continue
        seen.add(url)

        if kind == "SKIP":
            print(f"SKIP data: URI (not allowed on GitHub)")
            fails += 1
            continue

        if kind.startswith("REL:"):
            rel = kind[4:]
            ok = (ROOT / rel).exists()
            print(f"{'OK  ' if ok else 'FAIL'} local  {rel}")
            fails += 0 if ok else 1
            continue

        status, body = probe(url)
        short = re.sub(r"^https://", "", url)
        short = re.sub(r"(style|logo|color|logoColor|label|cache_seconds)=[^&]*", "", short)
        short = short[:96]

        if status != 200:
            print(f"FAIL {status}  {short}")
            fails += 1
        elif BAD_PATTERNS.search(body[:6000]):
            msg = BAD_PATTERNS.search(body[:6000]).group(0)
            print(f"FAIL 200 but body says {msg!r}  {short}")
            fails += 1
        elif "<svg" not in body[:2000]:
            print(f"FAIL 200 but not an SVG  {short}")
            fails += 1
        else:
            kb = len(body) // 1024
            print(f"OK   200 svg ({kb} KB)  {short}")
        time.sleep(0.6)

    print("-" * 64)
    if fails:
        print(f"{fails} image(s) need attention")
        return 1
    print(f"All {len(seen)} images verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())