#!/usr/bin/env python3
"""
Generate the hand-crafted SVG cards used by the GitHub profile README.

Why hand-crafted SVG instead of an <img> from a third-party service?
  * it renders inside github.com's markdown pipeline (images are allowed, raw HTML is not)
  * no external dependency, no rate limits, no caching surprises
  * fonts come from the system stack, gradients/animations run natively in the browser
  * change the palette in one place (PALETTE) and re-run:  python3 tools/gen_cards.py

Usage:  python3 tools/gen_cards.py [output_dir]
"""
from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- palette ---
PALETTE = {
    "bg0": "#0C1017", "bg1": "#080A10", "line": "#FFFFFF",
    "text": "#E9EDF6", "dim": "#97A1B5", "faint": "#6C7689",
    "violet": "#8B5CF6", "cyan": "#22D3EE", "emerald": "#34D399",
    "amber": "#FBBF24", "rose": "#FB7185", "pink": "#F472B6",
}
AURORA = "".join(
    f'<radialGradient id="{n}" cx=".5" cy=".5" r=".5">'
    f'<stop stop-color="{c}" stop-opacity="{o}"/>'
    f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
    for n, c, o in (("b1", PALETTE["violet"], .5), ("b2", PALETTE["cyan"], .34), ("b3", PALETTE["emerald"], .26))
)
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"


def hex_to_int(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def chip(x: float, y: float, w: float, h: float, label: str, color: str) -> str:
    r, g, b = hex_to_int(color)
    return (
        f'<g>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" '
        f'fill="rgb({r},{g},{b})" fill-opacity=".10" stroke="rgb({r},{g},{b})" stroke-opacity=".38"/>'
        f'<circle cx="{x + 15:.1f}" cy="{y + h / 2:.1f}" r="3.5" fill="rgb({r},{g},{b})"/>'
        f'<text x="{x + 26:.1f}" y="{y + h / 2 + 4.2:.1f}" class="sans" font-size="12.5" '
        f'fill="{PALETTE["text"]}">{escape(label)}</text>'
        f'</g>'
    )


# --- text metrics -----------------------------------------------------------
# We cannot measure fonts in Python, so approximate the advance width of the
# ui-sans-serif fallback stack at 12.5px. Uppercase and wide glyphs (M, W) are
# counted heavier than lowercase; "W" at ~1.0em is the worst case in our labels.
_NARROW = set("i j l t f r I . , ; : ' ! | ( ) [ ] ")
_WIDE = set("m w M W @ %")


def text_width(label: str, size: float = 12.5) -> float:
    """Approximate rendered width of `label` in px. Deliberately generous so a
    label never overflows its chip on a machine with a wider system font."""
    em = 0.0
    for ch in label:
        if ch in _NARROW:
            em += 0.34
        elif ch in _WIDE:
            em += 0.92
        elif ch.isupper():
            em += 0.72
        else:
            em += 0.565
    return em * size


def chip_width(label: str, size: float = 12.5) -> float:
    return text_width(label, size) + 38          # 26px left pad + 12px right pad


def wrap_chips(items: list[tuple[str, str]], max_w: float, gap: float = 8.0,
               row_h: float = 32.0) -> list[list[tuple[str, str, float]]]:
    """Lay chips out left-to-right, wrapping at max_w. Returns rows of
    (label, colour, width) so the caller can size the card afterwards."""
    rows: list[list[tuple[str, str, float]]] = [[]]
    used = 0.0
    for label, color in items:
        w = chip_width(label)
        add = w if not rows[-1] else w + gap
        if used + add > max_w and rows[-1]:
            rows.append([])
            used = 0.0
            add = w
        rows[-1].append((label, color, w))
        used += add
    return rows


def stack_svg() -> str:
    groups = [
        ("Frontend", [
            ("TypeScript", "#3178c6"), ("JavaScript", "#f0db4f"), ("Angular", "#dd0031"),
            ("React", "#61dafb"), ("Next.js", "#e9e9e9"), ("PrimeNG", "#a855f7"),
            ("Tailwind", "#38bdf8"), ("HTML", "#e34f26"), ("CSS", "#1572b6"),
        ]),
        ("Backend & data", [
            ("Node.js", "#5fa04e"), ("Express", "#d8d8d8"), ("PostgreSQL", "#4169e1"),
            ("MongoDB", "#4db33d"), ("Redis", "#dc382d"), ("SQLite", "#0b80d3"),
            ("Python", "#3776ab"), ("FastAPI", "#009688"), ("Zod / JWT", "#f59e0b"),
        ]),
        ("Cloud & tooling", [
            ("AWS", "#ff9900"), ("EC2 / S3", "#ed7100"), ("Bedrock", "#a259ff"),
            ("Docker", "#2496ed"), ("GCP Storage", "#4285f4"), ("Firebase", "#ffca28"),
            ("Nginx", "#009639"), ("Git", "#f05032"), ("GitHub Actions", "#2088ff"),
        ]),
        ("Craft", [
            ("tree-sitter", "#a8d6ba"), ("semgrep", "#c4b5fd"), ("Stripe", "#635bff"),
            ("Razorpay", "#22c1c3"), ("OpenAPI", "#6ce5a8"), ("Linux", "#f4c542"),
            ("C / Kernel", "#a8b9cf"), ("PHP", "#777bb4"), ("Go", "#00add8"),
        ]),
    ]

    pad, inner_gap = 14, 16
    card_w = 872
    chip_max = card_w - 2 * pad
    row_h, chip_h = 34, 30

    body, y = [], pad
    for title, items in groups:
        rows = wrap_chips(items, chip_max)
        card_h = 40 + len(rows) * row_h + 14
        body.append(f'<rect x="{pad}" y="{y}" width="{card_w}" height="{card_h}" rx="14" '
                    f'fill="#FFFFFF" fill-opacity=".028" stroke="#FFFFFF" stroke-opacity=".08"/>')
        body.append(f'<text x="{pad + 16}" y="{y + 26}" class="mono" font-size="11" '
                    f'letter-spacing="2.2" fill="{PALETTE["faint"]}">{escape(title.upper())}</text>')
        cy = y + 40
        for row in rows:
            cx = pad + 14
            for label, color, w in row:
                body.append(chip(cx, cy, w, chip_h, label, color))
                cx += w + 8
            cy += row_h
        y += card_h + inner_gap

    h = y - inner_gap + pad
    w = card_w + 2 * pad

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="Technology stack">
  <title>Technology stack</title>
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
      <stop stop-color="{PALETTE['bg0']}"/><stop offset="1" stop-color="{PALETTE['bg1']}"/>
    </linearGradient>
    <linearGradient id="sline" x1="0" y1="0" x2="{w}" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="{PALETTE['violet']}"/><stop offset=".5" stop-color="{PALETTE['cyan']}"/>
      <stop offset="1" stop-color="{PALETTE['emerald']}"/>
    </linearGradient>
    {AURORA}
    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="60"/></filter>
    <clipPath id="clip"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18"/></clipPath>
    <style>
      .sans {{ font-family: {SANS}; }}
      .mono {{ font-family: {MONO}; }}
      @keyframes drift {{ 0%,100%{{transform:translate(0,0)}} 50%{{transform:translate(26px,-18px)}} }}
      .blob {{ animation: drift 22s ease-in-out infinite; }}
    </style>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="url(#sbg)"/>
    <g filter="url(#soft)">
      <circle class="blob" cx="60" cy="20" r="150" fill="url(#b1)"/>
      <circle cx="{w - 40}" cy="{h - 30}" r="150" fill="url(#b2)"/>
    </g>
    {''.join(body)}
  </g>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity=".1"/>
</svg>'''


# ------------------------------------------------------------------ main ----
if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
    out.mkdir(parents=True, exist_ok=True)
    (out / "stack.svg").write_text(stack_svg(), encoding="utf-8")
    print(f"✓ {out / 'stack.svg'}")