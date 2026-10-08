#!/usr/bin/env python3
"""
Publish the interactive profile to GitHub Pages via a committed `docs/` directory.

The publish directory is `docs/` because GitHub's Pages API only accepts `/` or
`/docs` as a source path; `/` would also expose README.md, tools/ and DESIGN.md
on the public site.

WHY NOT the actions/upload-pages-artifact workflow?
    It failed with "exit code 2" on every commit of this repo, and it pins
    actions that now emit Node.js 20 deprecation warnings. Pages can build
    straight from a branch, which needs no workflow, no artifact upload, no
    `pages: write` permission, and rebuilds automatically on every push.

WHAT GETS COPIED
    Only what the published page actually loads. The repo root also holds
    README.md, tools/, verify.sh and DESIGN.md, none of which belong on a
    public site.

    The SVG assets are shared with the README, so they are copied rather than
    moved — assets/ stays the single source of truth.

`verify.sh` re-runs --check to prove docs/ has not drifted from the sources.

Usage:
    python3 tools/publish_site.py           # sync docs/ from the sources
    python3 tools/publish_site.py --check   # exit 1 if docs/ is stale
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"

# (source, destination-relative-to-site)
FILES: list[tuple[str, str]] = [
    ("index.html", "index.html"),
    ("assets/styles.css", "assets/styles.css"),
    ("assets/app.js", "assets/app.js"),
    ("assets/favicon.svg", "assets/favicon.svg"),
    ("assets/hero.svg", "assets/hero.svg"),
    ("assets/typing.svg", "assets/typing.svg"),
    ("assets/status.svg", "assets/status.svg"),
    ("assets/stack.svg", "assets/stack.svg"),
    ("assets/divider.svg", "assets/divider.svg"),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main(argv: list[str]) -> int:
    check = "--check" in argv
    missing = [s for s, _ in FILES if not (ROOT / s).exists()]
    if missing:
        print("✗ missing source files: " + ", ".join(missing))
        return 1

    if check:
        stale: list[str] = []
        for src, dst in FILES:
            d = SITE / dst
            if not d.exists():
                stale.append(f"{dst} (absent)")
            elif sha(ROOT / src) != sha(d):
                stale.append(f"{dst} (out of date)")
        if stale:
            print("✗ docs/ has drifted from the sources:")
            for s in stale:
                print("   •", s)
            print("  run: python3 tools/publish_site.py")
            return 1
        print(f"✓ docs/ matches all {len(FILES)} source files")
        return 0

    # stray files from an older publish would be served as-is
    if SITE.exists():
        shutil.rmtree(SITE)
    for src, dst in FILES:
        d = SITE / dst
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / src, d)

    # Pages runs Jekyll by default, which drops files starting with "_".
    (SITE / ".nojekyll").write_text("", encoding="utf-8")

    total = sum((SITE / d).stat().st_size for _, d in FILES)
    print(f"✓ published {len(FILES)} files to docs/ ({total // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))