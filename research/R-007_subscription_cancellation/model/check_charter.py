"""Mechanical check of 00_RESEARCH_CHARTER.md structure (not a substitute for semantic review)."""
import re, sys, os
t = open(os.path.join(os.path.dirname(__file__), "..", "00_RESEARCH_CHARTER.md"), encoding="utf-8").read()
ok = True
for b in "ABCDEFGHIJKL":
    if not re.search(rf"^### {b}\. ", t, re.M):
        print("missing branch", b); ok = False
rows = re.findall(r"^\| ([A-L]\d?f?\d*) \| (.+)$", t, re.M)
beliefs = {}
for rid, rest in rows:
    cells = [c.strip() for c in rest.rstrip("|").split("|")]
    if rid in ("Item",) or len(cells) < 4:
        continue
    beliefs[rid] = cells
for b in "ABCDEFGHIJKL":
    ids = [k for k in beliefs if k.startswith(b)]
    if not ids:
        print("branch without WNTB rows", b); ok = False
    for k in ids:
        if any(c == "" for c in beliefs[k][:4]):
            print("empty field in", k); ok = False
stop = re.search(r"## 4\. Mapping.*?\n\n(.*?)\n\n", t, re.S).group(1)
for i in range(1, 11):
    line = [l for l in stop.splitlines() if l.startswith(f"| {i}.")]
    if not line or not re.search(r"\b[A-L]\d", line[0]):
        print("stop condition not mapped", i); ok = False
for h in range(1, 15):
    if f"H{h:02d}" not in t:
        print("hypothesis unmapped", h); ok = False
print("WNTB rows:", sorted(beliefs))
print("CHARTER CHECK", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
