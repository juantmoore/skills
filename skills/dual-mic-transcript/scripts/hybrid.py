"""Hybrid transcript: text from an app transcript (e.g. Wispr Flow), speakers + timestamps from the mics.

usage: hybrid.py <workdir> <outdir> <app_transcript.txt> [--fixes fixes.json] [--title T] [--date D]
                 [--participants "A, B"] [--source-name "Wispr Flow"]

App transcript format: one utterance per line, "Speaker label: text" (labels are ignored).
Steps:
 1. Word-align the app text to each mic's raw whisper words (both mics hear the whole room) to give
    every app word a session timestamp; words neither mic has are interpolated.
 2. Speaker per sentence = which mic was louder over its words; near-equal sentences follow their line.
 3. Sentences of 4+ words that neither mic corroborates (<35% of words) get [unclear].
 4. App text from before the mics started is kept as a separate preface; speech after the app stopped
    is filled in from merge.py's turns.json and marked [local mics only].
Needs merge.py to have run first (for turns.json). --fixes: JSON list of [regex, replacement] applied to text.
"""
import argparse, difflib, json, os, re
import numpy as np
from common import Session, norm, write_outputs, hms

ap = argparse.ArgumentParser()
ap.add_argument("workdir"); ap.add_argument("outdir"); ap.add_argument("app")
ap.add_argument("--fixes"); ap.add_argument("--title", default="Working session"); ap.add_argument("--date", default="")
ap.add_argument("--participants"); ap.add_argument("--source-name", default="the app transcript")
args = ap.parse_args()
S = Session(args.workdir)
FIXES = [(re.compile(a), b) for a, b in (json.load(open(args.fixes)) if args.fixes else [])]


def fix(t):
    for rx, b in FIXES:
        t = rx.sub(b, t)
    return t


texts = [l.split(":", 1)[1].strip() if ":" in l else l.strip() for l in open(args.app) if l.strip()]
lines = []
for t in texts:   # some apps split a word across lines ("…about M" / "CPs, you…")
    if lines and re.match(r"^[A-Z]{2,}s\b", t) and re.search(r"\b[A-Z]$", lines[-1]):
        lines[-1] += t
    else:
        lines.append(t)
sents = [(li, s.strip()) for li, t in enumerate(lines) for s in re.split(r"(?<=[.?!—])\s+", t) if s.strip()]
W, Wsent = [], []
for si, (li, s) in enumerate(sents):
    for w in s.split():
        if norm(w):
            W.append(norm(w)); Wsent.append(si)
Wsent = np.array(Wsent)

tS = np.full(len(W), np.nan); tE = np.full(len(W), np.nan); hits = np.zeros(len(W), int)
for key in ("a", "b"):
    R = [w for w in S.words(key) if w["n"]]
    sm = difflib.SequenceMatcher(None, W, [r["n"] for r in R], autojunk=False)
    for blk in sm.get_matching_blocks():
        if blk.size < 2:      # lone one-word matches are often coincidental
            continue
        for k in range(blk.size):
            i, r = blk.a + k, R[blk.b + k]
            if np.isnan(tS[i]):
                tS[i], tE[i] = r["s"], r["e"]
            elif abs(tS[i] - r["s"]) <= 3:
                tS[i], tE[i] = (tS[i] + r["s"]) / 2, (tE[i] + r["e"]) / 2
            hits[i] += 1
known = ~np.isnan(tS)
if known.sum() < 0.3 * len(W):
    raise SystemExit(f"Only {known.mean():.0%} of the app transcript matches the mic audio. Wrong file, or wrong session?")
idx = np.arange(len(W))
pre = idx < idx[known][0]
t_all = np.maximum.accumulate(np.interp(idx, idx[known], tS[known]))
e_all = np.where(known, tE, t_all + 0.3)

units = []
for si, (li, s) in enumerate(sents):
    m = np.flatnonzero(Wsent == si)
    if not len(m):
        continue
    if pre[m].all():
        units.append(dict(li=li, text=s, pre=True)); continue
    s0, s1 = float(t_all[m[0]]), float(max(e_all[m[-1]], t_all[m[0]] + 0.3))
    km = m[known[m]]
    d = float(np.median([S.diff(tS[k], tE[k])[0] for k in km])) if len(km) else S.diff(s0, s1)[0]
    units.append(dict(li=li, text=s, s=s0, e=s1, d=d, support=float(known[m].mean()), n=len(m), pre=False))
real = [u for u in units if not u["pre"]]
for u in real:
    if abs(u["d"]) < 2.0:
        u["d"] = 0.5 * u["d"] + 0.5 * float(np.mean([v["d"] for v in real if v["li"] == u["li"]]))
    u["spk"] = S.spk["a"] if u["d"] > 0 else S.spk["b"]
    u["unclear"] = u["n"] >= 4 and u["support"] < 0.35

last_t = float(np.nanmax(tE))
tail = [t for t in json.load(open(os.path.join(args.workdir, "turns.json"))) if t["s"] > last_t + 1.0]

turns = []
for u in real:
    txt = fix(u["text"]) + (" [unclear]" if u["unclear"] else "")
    if turns and turns[-1]["spk"] == u["spk"]:
        turns[-1]["text"] += " " + txt; turns[-1]["e"] = max(turns[-1]["e"], u["e"])
    else:
        turns.append(dict(spk=u["spk"], s=u["s"], e=u["e"], text=txt))
for t in tail:
    turns.append(dict(spk=t["spk"], s=t["s"], e=t["e"], text=fix(t["text"]) + " [local mics only]"))

cues = []
for u in real:   # one cue per sentence; long ones split at ~84 chars, time shared by length
    words = fix(u["text"]).split(); chunks, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > 84:
            chunks.append(cur); cur = []
        cur.append(w)
    chunks.append(cur)
    e = max(u["e"], u["s"] + 0.6); tot = sum(len(" ".join(c)) for c in chunks); acc = 0
    for c in chunks:
        cs = u["s"] + (e - u["s"]) * acc / tot; acc += len(" ".join(c))
        cues.append((cs, u["s"] + (e - u["s"]) * acc / tot, u["spk"], " ".join(c)))
cues += [(t["s"], t["e"], t["spk"], fix(t["text"])) for t in tail]

pre_text = fix(" ".join(u["text"] for u in units if u["pre"]))
write_outputs(args.outdir, turns, cues,
              dict(title=f"{args.title}: {S.spk['a']} & {S.spk['b']}", date=args.date,
                   participants=args.participants or f"{S.spk['a']}, {S.spk['b']}", total=S.total,
                   extra={"Source": f"{args.source_name} text; speakers and timestamps from the two mic recordings (see notes.md)"}),
              preface=(f"Before the mics started recording ({args.source_name} only; speakers not verified)", pre_text) if pre_text else None)
stats = dict(app_words=len(W), words_timed_by_mics=int(known.sum()), heard_by_both_mics=int((hits == 2).sum()),
             preroll_words=int(pre.sum()), tail_turns_from_mics=len(tail), turns=len(turns), sentences=len(real),
             srt_cues=len(cues), unclear_marks=sum(u["unclear"] for u in real),
             words={S.spk[k]: sum(u["n"] for u in real if u["spk"] == S.spk[k]) for k in "ab"}, total=hms(S.total))
json.dump(turns, open(os.path.join(args.workdir, "turns_hybrid.json"), "w"))
json.dump(stats, open(os.path.join(args.workdir, "hybrid_stats.json"), "w"), indent=1)
print(json.dumps(stats, indent=1))
