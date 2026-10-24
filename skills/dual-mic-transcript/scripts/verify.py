"""Sanity checks on a finished transcript.

usage: verify.py <workdir> <outdir> [--hybrid]

- near-duplicate lines under different speakers (bleed that slipped through)
- speech present across each mic's file boundaries
- long silences
- SRT validity
- speaker share; with --hybrid, speaker agreement with the mic-only merge
"""
import difflib, json, os, re, sys
from common import hms

work, outdir = sys.argv[1], sys.argv[2]
hybrid = "--hybrid" in sys.argv
cfg = json.load(open(os.path.join(work, "config.json")))
T = json.load(open(os.path.join(work, "turns_hybrid.json" if hybrid else "turns.json")))

dups = 0
for i, t in enumerate(T):
    for u in T[i + 1:i + 4]:
        if u["spk"] != t["spk"] and abs(u["s"] - t["s"]) < 3 and min(len(t["text"]), len(u["text"])) > 25:
            if difflib.SequenceMatcher(None, t["text"].lower(), u["text"].lower()).ratio() > 0.7:
                dups += 1; print("  possible duplicate:", t["text"][:70], "|", u["text"][:70])
print(f"near-duplicate cross-speaker turns: {dups}")

for k in ("a", "b"):
    for off in cfg["mics"][k]["file_offsets"][1:]:
        b = off + cfg[f"offset_{k}"]
        n = sum(1 for t in T if t["s"] - 30 < b < t["e"] + 30)
        print(f"mic {k} file boundary at {hms(b)}: {n} turns within ±30 s" + ("  <-- CHECK" if n == 0 else ""))

for a, b in zip(T, T[1:]):
    if b["s"] - a["e"] > 45:
        print(f"silence {hms(a['e'])}–{hms(b['s'])} ({b['s'] - a['e']:.0f} s)")

srt = open(os.path.join(outdir, "transcript.srt")).read().strip().split("\n\n")
def ts(x):
    h, m, r = x.split(":"); s, ms = r.split(","); return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
ok = all(int(c.split("\n")[0]) == i and ts(c.split("\n")[1].split(" --> ")[1]) >= ts(c.split("\n")[1].split(" --> ")[0])
         for i, c in enumerate(srt, 1))
print(f"SRT: {len(srt)} cues, valid={ok}")

words = {}
for t in T:
    words[t["spk"]] = words.get(t["spk"], 0) + len(t["text"].split())
tot = sum(words.values())
print("speaker share:", ", ".join(f"{k} {v / tot:.0%}" for k, v in words.items()))

if hybrid:
    def tw(TT):
        return [(re.sub(r"[^a-z0-9']", "", x.lower()), t["spk"]) for t in TT
                for x in re.sub(r"\[[^\]]*\]", "", t["text"]).split() if re.sub(r"[^a-z0-9']", "", x.lower())]
    h, o = tw(T), tw(json.load(open(os.path.join(work, "turns.json"))))
    sm = difflib.SequenceMatcher(None, [x[0] for x in h], [x[0] for x in o], autojunk=False)
    pairs = [(h[b.a + k][1], o[b.b + k][1]) for b in sm.get_matching_blocks() for k in range(b.size)]
    print(f"speaker agreement with the mic-only merge: {sum(x == y for x, y in pairs) / len(pairs):.1%} of {len(pairs)} shared words")
