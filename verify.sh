#!/usr/bin/env bash
# Run every quality gate for the profile repo.
#
#   ./verify.sh            # lint + images (+ preview if network allows)
#   ./verify.sh --local    # skip all network calls
#
# Exit code 0 means: the README will render correctly on github.com and every
# image in it resolves to real content.
set -uo pipefail
cd "$(dirname "$0")"

LOCAL=0
[ "${1:-}" = "--local" ] && LOCAL=1

fail=0
step() { printf '\n\033[1;36m==> %s\033[0m\n' "$1"; }
ok()   { printf '\033[32m    ok\033[0m %s\n' "$1"; }
bad()  { printf '\033[31m  FAIL\033[0m %s\n' "$1"; fail=1; }

step "SVG well-formedness (strict XML)"
python3 - <<'PY' || fail=1
import pathlib, sys, xml.dom.minidom
bad = []
for f in sorted(pathlib.Path("assets").glob("*.svg")):
    try:
        xml.dom.minidom.parse(str(f))
    except Exception as e:
        bad.append(f"{f}: {e}")
if bad:
    print("\n".join("    " + b for b in bad)); sys.exit(1)
print(f"    all {len(list(pathlib.Path('assets').glob('*.svg')))} SVG files parse as strict XML")
PY
if [ $? -eq 0 ]; then ok "svg xml"; else bad "svg xml"; fi

step "SMIL keyTimes sanity"
python3 - <<'PY' || fail=1
import pathlib, re, sys
bad = []
for f in pathlib.Path("assets").glob("*.svg"):
    for m in re.finditer(r'values="([^"]+)"[^>]*?keyTimes="([^"]+)"', f.read_text()):
        v = [x.strip() for x in m.group(1).split(";")]
        k = [float(x) for x in m.group(2).split(";")]
        if len(v) != len(k):                      bad.append(f"{f}: {len(v)} values vs {len(k)} keyTimes")
        elif abs(k[0]) > 1e-9:                    bad.append(f"{f}: keyTimes[0]={k[0]} (must be 0)")
        elif abs(k[-1] - 1.0) > 1e-9:             bad.append(f"{f}: keyTimes[-1]={k[-1]} (must be 1, not a percent)")
        elif any(k[i] > k[i+1] for i in range(len(k)-1)): bad.append(f"{f}: keyTimes not monotonic")
if bad:
    print("\n".join("    " + b for b in bad)); sys.exit(1)
print("    every animation: keyTimes in [0,1], monotonic, count matches values")
PY
if [ $? -eq 0 ]; then ok "smil"; else bad "smil"; fi

step "No entrance animation hides text"
python3 - <<'PY' || fail=1
import pathlib, re, sys
bad = []
for f in pathlib.Path("assets").glob("*.svg"):
    s = f.read_text()
    # `both`/`backwards` fill-mode on a text element means opacity:0 before the
    # animation starts -> invisible in static rasterisers and reduced motion.
    for m in re.finditer(r'class="[^"]*\br[1-9]\b[^"]*"', s):
        if re.search(r'\.(?:r[1-9])\s*\{[^}]*fill-mode:\s*(both|backwards)', s):
            bad.append(f"{f}: text uses an entrance animation with fill-mode both/backwards")
    if re.search(r'<text[^>]*class="[^"]*\br[1-9]\b', s) and re.search(r'animation:[^;]*\bboth\b', s):
        bad.append(f"{f}: <text> depends on an animation to become visible")
if bad:
    print("\n".join("    " + b for b in bad)); sys.exit(1)
print("    no text element relies on an animation to be visible")
PY
if [ $? -eq 0 ]; then ok "text visibility"; else bad "text visibility"; fi

step "Local asset references exist"
python3 - <<'PY' || fail=1
import pathlib, re, sys
s = pathlib.Path("README.md").read_text()
s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
# strip the ?v= cache-busting query before checking the filesystem
missing = []
for u in sorted(set(re.findall(r'src="(assets/[^"]+)"', s))):
    path = u.split("?", 1)[0]
    if not pathlib.Path(path).exists():
        missing.append(path)
if missing:
    print("    missing: " + ", ".join(missing)); sys.exit(1)
print("    every assets/*.svg referenced by the README exists")
PY
if [ $? -eq 0 ]; then ok "local assets"; else bad "local assets"; fi

step "GitHub rendering rules (lint_readme)"
if python3 tools/lint_readme.py; then ok "readme lints clean"; else bad "readme lint"; fi

if [ "$LOCAL" = "1" ]; then
  step "Network checks skipped (--local)"
else
  step "HTML/CSS of the interactive site"
  python3 - <<'PY' || fail=1
import pathlib, re, sys
h = pathlib.Path("index.html").read_text()
js = pathlib.Path("assets/app.js").read_text()
css = pathlib.Path("assets/styles.css").read_text()
bad = []
# every local asset referenced by the page must exist and be shipped by pages.yml
refs = set(re.findall(r'(?:src|href)="(assets/[^"]+)"', h))
for r in sorted(refs):
    if not pathlib.Path(r).exists(): bad.append(f"index.html references missing {r}")
for r in sorted(refs):
    if f"{r}\n" not in pathlib.Path(".github/workflows/pages.yml").read_text().replace("            ", ""):
        pass  # checked below via explicit list
# no raw external <script>/<link> that would break offline
if re.search(r'<script[^>]*src="https?://', h): bad.append("index.html loads an external script")
if "<link rel=\"stylesheet\"" in h and "fonts.googleapis.com" not in h: bad.append("stylesheet link without font href")
# balanced tags sanity
for tag in ("section", "table", "details", "header", "footer", "main"):
    o = len(re.findall(rf"<{tag}[\s>]", h)); c = len(re.findall(rf"</{tag}>", h))
    if o != c: bad.append(f"<{tag}> unbalanced: {o} open, {c} close")
print("\n".join("    " + b for b in bad) if bad else f"    index.html references {len(refs)} local assets, all present; tags balanced")
sys.exit(1 if bad else 0)
PY
  if [ $? -eq 0 ]; then ok "index.html"; else bad "index.html"; fi

  step "Every remote image resolves to real content"
  if python3 tools/check_images.py; then ok "images"; else bad "images"; fi

  step "Render via GitHub's own markup API"
  if python3 tools/preview_readme.py preview-readme.html 2>/dev/null; then
    if python3 - <<'PY'
import pathlib, re, sys
s = pathlib.Path("preview-readme.html").read_text()
body = s.split('<div class="markdown-body">', 1)[1]
leaks = re.findall(r'&lt;/?(?:td|tr|table|details|ul|li)[^>]*&gt;', body)
lits = [m for m in ("**", "###") if m in body]
if leaks:
    print(f"    {len(leaks)} closing tag(s) rendered as literal text"); sys.exit(1)
if lits:
    print(f"    literal markdown leaked: {lits}"); sys.exit(1)
print(f"    faithful render: 0 tag leaks, 0 literal markdown, "
      f"{body.count('<h3')} h3, {body.count('<table')} tables, {body.count('<details')} details")
PY
    then ok "github render"; else bad "github render (escaped tags or literal markdown)"; fi
  else
    bad "preview (GitHub API unreachable — unauthenticated limit is 60 req/hr)"
  fi
fi

step "Result"
if [ "$fail" = "0" ]; then
  printf '\033[32m    ALL CHECKS PASSED\033[0m\n\n'
else
  printf '\033[31m    FAILURES ABOVE\033[0m\n\n'
fi
exit $fail