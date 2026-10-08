#!/usr/bin/env python3
"""
Render README.md exactly the way github.com will — by asking GitHub itself.

Uses POST https://api.github.com/markdown (the same github/markup pipeline that
serves profile READMEs), so the preview reflects GFM semantics AND GitHub's HTML
sanitizer. This matters because GitHub's behaviour is counter-intuitive:

  * markdown separated from an HTML tag by a BLANK LINE is still processed
        <td>
        **bold**              ->  <strong>bold</strong>
        ### Heading           ->  <h3>Heading</h3>
        - item                ->  <ul><li>item</li></ul>
  * markdown on the SAME LINE as the tag is NOT processed
        <td>**bold**</td>     ->  literal asterisks
  * style / class / target are stripped; align / width / valign survive
  * iframe, script, style, svg and data: URIs are escaped away

If the API is unreachable (offline), falls back to a local renderer and says so.

Usage:  python3 tools/preview_readme.py [output.html]
"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com/markdown"


def render_with_github(md: str) -> tuple[str, str]:
    """Returns (html, engine). html is GitHub's sanitized GFM output."""
    # HTML comments are not rendered by GitHub; sending them only risks the
    # payload being rejected. Strip them first.
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    req = urllib.request.Request(
        API,
        data=json.dumps({"text": md, "mode": "gfm"}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "readme-preview",
                 "Accept": "application/vnd.github+json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
        # The endpoint returns JSON {"html": ...} normally, but can return the
        # rendered HTML directly depending on Accept negotiation. Handle both.
        stripped = raw.lstrip()
        if stripped.startswith("{"):
            return json.loads(stripped)["html"], "github markup API"
        return raw, "github markup API (raw)"
    except (urllib.error.URLError, KeyError, json.JSONDecodeError,
            TimeoutError, ValueError) as e:
        import warnings
        warnings.warn(
            f"GitHub markup API unavailable ({type(e).__name__}: {e}). "
            f"The offline fallback is only an approximation — verify layout on "
            f"github.com before pushing. Wait for the API rate limit to reset "
            f"(60 req/hr unauthenticated) for a faithful render.",
            RuntimeWarning, stacklevel=2,
        )
        return fallback_render(md), f"APPROXIMATE fallback ({type(e).__name__})"


def fallback_render(md: str) -> str:
    """Offline path: python-markdown with raw-HTML-block contents pre-rendered.

    This approximates GFM but is NOT faithful for deeply nested raw HTML
    (details inside td, html tables inside details). When it is used, the caller
    gets a warning so a broken fallback is never mistaken for the real render.
    """
    import warnings
    try:
        import markdown  # type: ignore
    except ImportError:
        warnings.warn(
            "python-markdown is not installed -> falling back to raw text. "
            "Install it (pip install markdown) or run with network access.",
            RuntimeWarning, stacklevel=2,
        )
        return "<pre>" + html.escape(md) + "</pre>"

    BLOCK = r"(table|details|div|p|td|th|blockquote|ul|ol|li|figure)"
    # split on blank-line separated HTML blocks and render the inside separately
    parts = re.split(rf"(?m)^(?=\s*<{BLOCK}[\s>])", md)
    out = []
    for part in parts:
        m = re.match(rf"^(\s*<{BLOCK}[\s>].*?)$", part, re.S)
        if not m:
            out.append(markdown.markdown(part, extensions=["tables", "sane_lists"]))
            continue
        opening = re.match(r"^\s*<([a-z]+)[\s>].*?>", part, re.S)
        tag = opening.group(1) if opening else "div"
        head = re.match(r"^\s*<[a-z]+[\s>][^\n]*\n?", part).group(0)
        body = re.sub(rf"^\s*<{tag}[\s>][^\n]*\n?", "", part)
        body = re.sub(rf"\s*</\s*{tag}\s*>\s*$", "", body)
        inner = markdown.markdown(body, extensions=["tables", "sane_lists"])
        out.append(head + inner + f"</{tag}>")
    return "\n".join(out)


def build() -> str:
    md = (ROOT / "README.md").read_text(encoding="utf-8")
    body, engine = render_with_github(md)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>README preview — github.com/its-skark</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; background:#010409; color:#e6edf3;
         font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif; }}
  .page {{ max-width:1012px; margin:0 auto; padding:24px 32px 120px; }}
  /* GitHub's README container is ~890px wide inside the repo page */
  .markdown-body {{ max-width:890px; }}
  .markdown-body img {{ max-width:100%; vertical-align:middle; box-sizing:content-box; }}
  .markdown-body table {{ border-collapse:collapse; display:block; width:max-content;
                          max-width:100%; overflow:auto; }}
  .markdown-body td,.markdown-body th {{ border:1px solid #3d444d; padding:8px 13px; vertical-align:top; }}
  .markdown-body tr {{ border-top:1px solid #3d444d; background:#0d1117; }}
  .markdown-body tr:nth-child(2n) {{ background:#151b23; }}
  .markdown-body h1,.markdown-body h2,.markdown-body h3,.markdown-body h4 {{ margin:24px 0 16px;
         font-weight:600; line-height:1.25; }}
  .markdown-body h1 {{ font-size:2em; padding-bottom:.3em; border-bottom:1px solid #21262d; }}
  .markdown-body h2 {{ font-size:1.5em; padding-bottom:.3em; border-bottom:1px solid #21262d; }}
  .markdown-body h3 {{ font-size:1.25em; }}
  .markdown-body p,.markdown-body ul,.markdown-body ol {{ margin:0 0 16px; }}
  .markdown-body ul,.markdown-body ol {{ padding-left:2em; }}
  .markdown-body li {{ margin:.25em 0; }}
  .markdown-body li>p {{ margin:0 0 8px; }}
  .markdown-body a {{ color:#4493f8; text-decoration:none; }}
  .markdown-body code {{ background:#1f2530; padding:.2em .4em; border-radius:6px; font-size:85%;
         font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .markdown-body pre {{ background:#151b23; padding:16px; border-radius:6px; overflow:auto; }}
  .markdown-body details {{ margin:16px 0; border:1px solid #3d444d; border-radius:8px; padding:12px 14px; }}
  .markdown-body summary {{ cursor:pointer; font-weight:600; }}
  .markdown-body hr {{ height:1px; border:0; background:#3d444d; margin:24px 0; }}
  .markdown-body sub {{ font-size:.75em; color:#8b949e; }}
  .banner {{ position:sticky; top:0; z-index:9; background:#010409f2; backdrop-filter:blur(8px);
             border-bottom:1px solid #21262d; padding:9px 32px; font:12px ui-monospace,monospace;
             color:#8b949e; display:flex; gap:18px; justify-content:space-between; }}
  .banner b {{ color:#3fb950; }}
  .engine {{ color:#d29922; }}
</style></head>
<body>
<div class="banner">
  <span>README preview · github.com/<b>its-skark</b> · renderer: <span class="engine">{engine}</span></span>
  <span>container width 1012px</span>
</div>
<div class="page"><div class="markdown-body">
{body}
</div></div>
</body></html>"""


if __name__ == "__main__":
    dest = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "preview-readme.html")
    html = build()
    dest.write_text(html, encoding="utf-8")
    engine = re.search(r'class="engine">([^<]+)<', html)
    print(f"✓ {dest}  (engine: {engine.group(1) if engine else '?'})")