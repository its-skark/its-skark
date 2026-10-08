#!/usr/bin/env python3
"""
Regression guard for status.svg: text must never spill past the card border.

The bug this prevents: row 3's sub-line had its baseline at y=193 with
descenders reaching ~y=198, but the card was only 196 tall. The text was
clipped mid-glyph by the rounded border, which read as stray/garbled text at the
bottom of the banner.

Also checks that each animated bar is centred on its two-line row, and that the
accent widths are uniform (unequal widths implied progress data that does not
exist).

Usage:  python3 tools/check_status_layout.py
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESC = 0.22      # descender depth as a fraction of font-size
TITLE_PX = 15
SUB_PX = 12


def main() -> int:
    p = ROOT / "assets" / "status.svg"
    svg = p.read_text(encoding="utf-8")
    problems: list[str] = []

    h = int(re.search(r'viewBox="0 0 (\d+) (\d+)"', svg).group(2))
    inner = h - 2                                   # inside the 1px border

    titles = [int(m) for m in re.findall(r'<text x="66" y="(\d+)" font-size="15"', svg)]
    subs = [int(m) for m in re.findall(r'<text class="mono" x="66" y="(\d+)"', svg)]
    if len(titles) != len(subs):
        problems.append(f"{len(titles)} titles vs {len(subs)} sub-lines")
    else:
        for i, (t, s) in enumerate(zip(titles, subs), 1):
            bottom = s + SUB_PX * DESC
            if bottom > inner:
                problems.append(
                    f"row {i}: sub-line descender reaches {bottom:.1f} but the card "
                    f"ends at {inner} (clipped by {bottom - inner:.1f}px)"
                )

    bars = re.findall(r'class="grow g\d" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)"', svg)
    widths = {round(float(w), 1) for _, _, w in bars}
    if len(widths) > 1:
        problems.append(f"accent bars have unequal widths {sorted(widths)} "
                        f"(implies fake progress data)")
    if len(bars) != len(titles):
        problems.append(f"{len(bars)} bars vs {len(titles)} rows")
    else:
        # bars are declared in the same order as the rows they belong to
        for i, ((_, by, _), t, s) in enumerate(zip(bars, titles, subs), 1):
            centre = (t + s) / 2
            got = float(by) + 2          # bar is 4 tall, so its centre is y+2
            if abs(got - centre) > 1.5:
                problems.append(
                    f"row {i}: bar centre {got} vs row centre {centre:.1f} "
                    f"(off by {got - centre:+.1f}px)"
                )

    if problems:
        print(f"✗ {len(problems)} status.svg layout problem(s):")
        for x in problems:
            print("  •", x)
        return 1

    print(f"✓ status.svg: card {h} tall, {len(titles)} rows clear the border, "
          f"bars centred and uniform")
    return 0


if __name__ == "__main__":
    sys.exit(main())