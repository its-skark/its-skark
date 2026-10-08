#!/usr/bin/env python3
"""
Generate assets/typing.svg — an animated typewriter banner that GitHub can render.

Why not readme-typing-svg.herokuapp.com / demolab.com? Those endpoints now return
the demo site's HTML instead of an SVG for most parameter combinations (verified
2026-10-08), and two other popular card services already return HTTP 402. Other
services (github-profile-trophy, github-readme-activity-graph) are dead, and
githack/jsDelivr cannot serve HTML to a README anyway (iframe is stripped by
GitHub's sanitizer). Self-hosting the SVG is the robust 2026 answer.

Technique: every line shares ONE timeline. Each line's visible width is animated
through keyTimes computed from a single phase table, so lines type in sequence,
hold together, then erase together — they can never drift out of sync or get
permanently stuck invisible.

Usage:  python3 tools/gen_typing_svg.py [output_dir]
"""
from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

# ------------------------------------------------------------------ config --
LINES: list[tuple[str, str]] = [
    ("full-stack typescript engineer", "#7CE7F5"),
    ("angular · react · node · postgres", "#C4B5FD"),
    ("python · tree-sitter · aws bedrock", "#6EE7B7"),
    ("shipping saas, pos & code-intelligence tools", "#FCD34D"),
]

SIZE = 21          # px
LH = 34            # line height
X = 56             # text origin
TOP = 30           # first baseline
ADV = 0.6          # monospace advance ratio (em)
PAD = 12           # clip slack so the final glyph is never cut

# ---- single shared timeline (seconds) --------------------------------------
TYPE_START = 0.35     # when typing begins
TYPE_TIME = 1.5 # per-line typing duration
STAGGER = 0.42        # delay between consecutive lines starting to type
HOLD_END = 8.0        # when the erase phase begins
ERASE_TIME = 1.1      # per-line erase duration
ERASE_STAGGER = 0.22  # delay between consecutive lines starting to erase
TOTAL = 10.4          # one full loop, then repeat

BG_W = 790
BG_H = TOP + LH * (len(LINES) - 1) + 30
WIDTHS = [len(t) * SIZE * ADV + PAD for t, _ in LINES]


def frac(t: float) -> str:
    """SMIL keyTimes are FRACTIONS in [0, 1], not percentages.
    Passing 3.36 instead of 0.0336 makes the whole <animate> invalid, and the
    browser silently ignores it — the element keeps its base value forever."""
    return f"{t / TOTAL:.5f}"


def line_xml(i: int) -> str:
    """One line: clip rect + caret, both driven by the same shared keyTimes."""
    text, color = LINES[i]
    w = WIDTHS[i]
    y = TOP + i * LH

    t0 = TYPE_START + i * STAGGER          # typing starts
    t1 = t0 + TYPE_TIME                    # fully typed
    e0 = HOLD_END + i * ERASE_STAGGER      # erasing starts
    e1 = e0 + ERASE_TIME                   # fully erased

    times = [0.0, t0, t1, e0, e1, TOTAL]
    vals = f"0;0;{w:.1f};{w:.1f};0;0"
    keytimes = ";".join(frac(t) for t in times)

    # caret travels with the clip edge and fades out once the line is erased
    caret_x = [X - 6, X - 6, X + w - PAD + 2, X + w - PAD + 2, X - 6, X - 6]
    caret_o = "0;1;1;1;0;0"
    ctimes = ";".join([
        frac(0), frac(max(t0 - 0.05, 0)), frac(t0 + 0.25), frac(e0),
        frac(e0 + 0.05), frac(TOTAL),
    ])

    return f'''
  <g>
    <clipPath id="clip{i}">
      <rect x="{X - 8}" y="{y - SIZE - 8}" width="0" height="{SIZE + 18}">
        <animate attributeName="width" values="{vals}" keyTimes="{keytimes}"
                 dur="{TOTAL}s" repeatCount="indefinite" calcMode="linear"/>
      </rect>
    </clipPath>
    <g clip-path="url(#clip{i})">
      <text class="mono" x="{X}" y="{y}" font-size="{SIZE}" fill="{color}"
            xml:space="preserve">{escape(text)}</text>
    </g>
    <rect x="{X - 6}" y="{y - SIZE - 1}" width="10" height="{SIZE - 2}" rx="2" fill="#22D3EE" opacity="0">
      <animate attributeName="x" values="{' ; '.join(f'{v:.1f}' for v in caret_x).replace(' ; ', ';')}"
               keyTimes="{ctimes}" dur="{TOTAL}s" repeatCount="indefinite" calcMode="linear"/>
      <animate attributeName="opacity" values="{caret_o}" keyTimes="{ctimes}"
               dur="{TOTAL}s" repeatCount="indefinite" calcMode="linear"/>
    </rect>
  </g>'''


def build() -> str:
    mono = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
    sans = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    alt = "; ".join(t for t, _ in LINES)

    lines = "\n".join(line_xml(i) for i in range(len(LINES)))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BG_W}" height="{BG_H}" viewBox="0 0 {BG_W} {BG_H}" fill="none" role="img" aria-label="Rachit Pandey — {escape(alt)}">
  <title>its-skark — animated typewriter banner</title>
  <desc>Static fallback text: {escape(alt)}.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{BG_W}" y2="{BG_H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0C1017"/><stop offset="1" stop-color="#080A10"/>
    </linearGradient>
    <linearGradient id="tg" x1="0" y1="0" x2="{BG_W}" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#8B5CF6"/><stop offset=".5" stop-color="#22D3EE"/>
      <stop offset="1" stop-color="#34D399"/>
    </linearGradient>
    <radialGradient id="g1" cx=".5" cy=".5" r=".5">
      <stop stop-color="#8B5CF6" stop-opacity=".28"/><stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx=".5" cy=".5" r=".5">
      <stop stop-color="#22D3EE" stop-opacity=".20"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/>
    </radialGradient>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="44"/></filter>
    <clipPath id="frame"><rect x="1" y="1" width="{BG_W - 2}" height="{BG_H - 2}" rx="16"/></clipPath>
    <style>
      .mono {{ font-family: {mono}; }}
      .sans {{ font-family: {sans}; }}
      @keyframes blink {{ 0%,48%{{opacity:1}} 49%,100%{{opacity:0}} }}
      .caret {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes drift {{ 0%,100%{{transform:translate(0,0)}} 50%{{transform:translate(24px,-11px)}} }}
      .blob {{ animation: drift 20s ease-in-out infinite; }}
    </style>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{BG_W}" height="{BG_H}" fill="url(#bg)"/>
    <g filter="url(#soft)">
      <circle class="blob" cx="80" cy="8" r="110" fill="url(#g1)"/>
      <circle cx="{BG_W - 50}" cy="{BG_H - 8}" r="110" fill="url(#g2)"/>
    </g>

    <rect x="1" y="1" width="3" height="{BG_H - 2}" fill="url(#tg)"/>

    <!-- shell prompt: static, always visible, never animated away -->
    <text class="mono" x="18" y="{TOP}" font-size="{SIZE}" fill="#8B5CF6">$</text>
    <rect class="caret" x="{X - 6}" y="{TOP - SIZE - 1}" width="10" height="{SIZE - 2}" rx="2" fill="#22D3EE" opacity=".9"/>

    {lines}
  </g>

  <rect x="1" y="1" width="{BG_W - 2}" height="{BG_H - 2}" rx="16" fill="none" stroke="#FFFFFF" stroke-opacity=".1"/>
</svg>'''


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
    out.mkdir(parents=True, exist_ok=True)
    (out / "typing.svg").write_text(build(), encoding="utf-8")
    print(f"✓ {out / 'typing.svg'}  ({BG_W}x{BG_H}, {TOTAL}s loop)")