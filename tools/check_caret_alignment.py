#!/usr/bin/env python3
"""
Regression guard for the typewriter banner's caret alignment.

The bug this prevents: the caret's rest position was derived from an assumed
monospace advance (0.6em) rather than the width the browser actually laid out,
so it drifted a few px past the last glyph — worst on lines containing "·".

The banner now sets `textLength` + `lengthAdjust="spacing"` on every line, which
forces the renderer to use exactly len(text) * SIZE * ADV px regardless of which
system monospace font resolves. That makes the geometry deterministic:

    caret_rest_x  ==  X + textLength - 1

This script verifies that invariant holds for every line, using the generator's
own constants, and that no second (static) caret is left at the prompt.

Usage:  python3 tools/check_caret_alignment.py
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from gen_typing_svg import ADV, LINES, SIZE, TEXT_W, X  # noqa: E402

TOL = 1.5  # px; -1px offset is intentional so the caret hugs the last glyph


def main() -> int:
    svg = (ROOT / "assets" / "typing.svg").read_text(encoding="utf-8")
    problems: list[str] = []

    # 1. every line must declare an exact width
    declared = [float(v) for v in re.findall(r'textLength="([\d.]+)"', svg)]
    if len(declared) != len(LINES):
        problems.append(f"{len(declared)} textLength attrs, expected {len(LINES)}")
    if len(re.findall(r'lengthAdjust="spacing"', svg)) != len(LINES):
        problems.append("not every line has lengthAdjust=\"spacing\"")

    for (text, _), want, got in zip(LINES, TEXT_W, declared):
        if abs(want - got) > 0.05:
            problems.append(f"{text[:24]!r}: textLength {got} != {want}")

    # 2. caret must park flush against the end of that exact width
    homes = [float(v) for v in re.findall(r'<rect x="([\d.]+)" y="\d+" width="10"', svg)]
    rests = re.findall(r'<animate attributeName="x" values="([^"]+)"', svg)
    if len(rests) != len(LINES):
        problems.append(f"{len(rests)} caret x-animations, expected {len(LINES)}")
    for (text, _), home, vals in zip(LINES, homes, rests):
        steps = [float(v) for v in vals.split(";")]
        if len(steps) != 6:
            problems.append(f"{text[:24]!r}: caret has {len(steps)} stops, expected 6")
            continue
        if abs(steps[0] - home) > 0.05:
            problems.append(f"{text[:24]!r}: caret base x {steps[0]} != rect x {home}")
        expected = X + len(text) * SIZE * ADV - 1
        for label, got in (("hold", steps[2]), ("hold-end", steps[3])):
            if abs(got - expected) > TOL:
                problems.append(
                    f"{text[:24]!r}: caret {label} x={got}, expected {expected:.1f} "
                    f"(off by {got - expected:+.1f}px)"
                )

    # 3. exactly one caret per line, and no leftover static caret at the prompt
    carets = re.findall(r'fill="#22D3EE"[^>]*opacity="0"', svg)
    if len(carets) != len(LINES):
        problems.append(f"{len(carets)} animated carets, expected {len(LINES)}")
    if 'class="caret"' in svg:
        problems.append("a static prompt caret is still present (renders as two cursors)")

    if problems:
        print(f"✗ {len(problems)} caret/alignment problem(s):")
        for p in problems:
            print("  •", p)
        return 1

    print(f"✓ typewriter: {len(LINES)} lines, exact textLength, "
          f"caret flush at X+width-1, single cursor")
    return 0


if __name__ == "__main__":
    sys.exit(main())