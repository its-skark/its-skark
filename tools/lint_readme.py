#!/usr/bin/env python3
"""
Lint README.md for markdown constructs that GitHub will NOT render as intended.

Ground truth for this lint comes from GitHub's own markup API:
    POST https://api.github.com/markdown  {"text": "...", "mode": "gfm"}

Verified behaviours (2026-10-08):
  * pipe tables: `**bold**` IS processed
  * raw HTML blocks (<table>, <div align>, <details>, <p align>): `**bold**`,
    `_em_` and `` `code` `` are NOT processed -> they render as literal asterisks
  * `target="_blank"` is stripped (not in GitHub's attribute allowlist)
  * style/class/id are stripped; align/width/valign on table cells are kept
  * <iframe>, <style>, <script>, inline style and data: URIs are removed

Usage:  python3 tools/lint_readme.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_BLOCK_TAGS = ("table", "div", "details", "p", "td", "tr", "ul", "ol", "li",
                   "blockquote", "figure", "details")

VOID = {"br", "hr", "img", "input", "meta", "link", "wbr", "col", "area", "base",
        "embed", "source", "track"}


def is_inline_html(fragment: str) -> bool:
    """True when `fragment` is plain text wrapped in inline HTML tags, with every
    non-tag character sitting inside an element. This distinguishes an
    intentional all-HTML table cell from markdown text that GitHub would
    mis-render. Written as a tiny state machine rather than a regex because the
    content contains characters like `->` and `·`."""
    depth = 0
    saw_tag = False
    i = 0
    while i < len(fragment):
        if fragment[i] != "<":
            # bare text is only allowed inside an open inline element
            if depth == 0:
                if fragment[i].strip() == "":
                    i += 1
                    continue
                return False
            # consume until the next '<'
            nxt = fragment.find("<", i)
            if nxt == -1:
                i = len(fragment)
                continue
            i = nxt
            continue
        end = fragment.find(">", i)
        if end == -1:
            return False
        tag = fragment[i + 1:end].strip().rstrip("/").strip()
        closing = tag.startswith("/")
        name = re.match(r"^/?\s*([a-zA-Z][a-zA-Z0-9]*)", tag)
        if not name:
            return False
        saw_tag = True
        name = name.group(1).lower()
        if closing:
            depth -= 1
            if depth < 0:
                return True          # e.g. the cell's own </td>
        elif name not in VOID:
            depth += 1
        i = end + 1
    return saw_tag


def raw_html_regions(text: str) -> list[tuple[int, int, str]]:
    """Line ranges that sit inside a raw HTML block, where inline markdown is
    not processed by GitHub."""
    regions: list[tuple[int, int, str]] = []
    lines = text.splitlines()
    in_block = False
    start = 0
    tag = ""
    for i, line in enumerate(lines, 1):
        if not in_block:
            m = re.match(r"\s*<(" + "|".join(RAW_BLOCK_TAGS) + r")[\s>]", line, re.I)
            if m:
                in_block, start, tag = True, i, m.group(1).lower()
        else:
            if re.search(rf"</\s*{tag}\s*>", line, re.I) or re.match(rf"\s*</\s*{tag}\s*>", line, re.I):
                regions.append((start, i, tag))
                in_block = False
    if in_block:
        regions.append((start, len(lines), tag))
    return regions


def main() -> int:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    # 1. inline markdown inside raw HTML blocks -> literal text on GitHub
    for start, end, tag in raw_html_regions(text):
        lines = text.splitlines()[start - 1:end]
        for off, line in enumerate(lines):
            n = start + off
            if line.lstrip().startswith("<!--"):
                continue
            for m in re.finditer(r"\*\*[^*\n]+\*\*|(?<!\w)_[^_\n]+_(?!\w)", line):
                frag = m.group(0)
                if re.search(r"<(b|strong|em|i|code)>", line):
                    continue  # already handled with html tags
                problems.append(
                    f"line {n}: `{frag}` inside <{tag}> renders LITERALLY on GitHub "
                    f"(inline markdown is not processed in raw HTML blocks) -> use <b>…</b>"
                )

    # 2. attributes GitHub strips
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r'\starget\s*=', line):
            problems.append(f"line {i}: target= is stripped by GitHub's sanitizer")
        if re.search(r'\sstyle\s*=\s*"[^"]*float', line):
            problems.append(f"line {i}: inline style= is stripped; use align=\"right\"")
        if 'data:' in line and re.search(r'src\s*=\s*"data:', line):
            problems.append(f"line {i}: data: URI images are not allowed")

    # 2b. A raw HTML *block* element whose tag is not alone on its line makes cmark
    #     treat the whole run as raw HTML, so trailing markdown stops being parsed
    #     and following closing tags can be emitted as literal text. Verified
    #     against the GitHub markup API: `<summary>x</summary>` on one line is
    #     fine (it is a complete element), but a *block* container like
    #     `<details>text` swallows what follows.
    in_comment = False
    for i, line in enumerate(text.splitlines(), 1):
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        for m in re.finditer(r"<(details|table|div|td|th|tr|ul|ol|blockquote|figure)\b[^>]*>", line, re.I):
            rest = line[m.end():].strip()
            tag = m.group(1).lower()
            if not rest:
                continue
            # A cell/row whose entire content is inline HTML on the same line is
            # fine: it needs no markdown. The bug is when *markdown-style* text
            # follows on the same line, because then the author expected it to be
            # parsed and it will not be.
            if re.match(rf"^</\s*{tag}\s*>", rest, re.I):
                continue
            if is_inline_html(rest):
                continue  # cell holds only inline HTML -> intentional
            problems.append(
                f"line {i}: <{tag}> is followed by non-HTML text on the same line "
                f"({rest[:48]!r}) — cmark treats the whole block as raw HTML, so it "
                f"will render literally; move it to its own line"
            )

    # 3. img tags need alt text (skip HTML comments — they never render)
    in_comment = False
    for i, line in enumerate(text.splitlines(), 1):
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        for m in re.finditer(r"<img\b[^>]*>", line):
            if "alt=" not in m.group(0):
                problems.append(f"line {i}: <img> without alt text")

    if not problems:
        print("✓ README lints clean: no literal-markdown-in-raw-HTML, no stripped attrs.")
        return 0

    print(f"✗ {len(problems)} issue(s):\n")
    for p in problems:
        print("  •", p)
    return 1


if __name__ == "__main__":
    sys.exit(main())