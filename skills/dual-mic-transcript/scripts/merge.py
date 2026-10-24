"""Mic-only transcript: merge both mics' whisper output into one speaker-labeled conversation.

usage: merge.py <workdir> <outdir> [--title T] [--date D]

Each mic hears both people, so whisper transcribes both voices on both tracks. For every word,
the level difference between the mics decides who said it; each speaker's words are then taken
ONLY from their own mic's transcript (clearer audio, intact word order) and the other copy is
dropped as bleed. Writes transcript.md/.txt/.srt to outdir and turns.json + merge_stats.json to workdir.
"""
import argparse, json, os, re
import numpy as np
from common import Session, write_outputs, hms

ap = argparse.ArgumentParser()
ap.add_argument("workdir"); ap.add_argument("outdir")
ap.add_argument("--title", default="Working session"); ap.add_argument("--date", default="")
args = ap.parse_args()
S = Session(args.workdir)
floor = S.floor()
CONFIDENT_DB = 2.5     # a word this far from the boundary decides its own speaker
STOCK = {"thankyou", "thanksforwatching", "byebye", "you", "thankyouforwatching"}   # whisper silence hallucinations


def load(key):
    """Words this mic's wearer said (key 'a' or 'b'), plus the marginal words it gave away."""
    sign = 1 if key == "a" else -1
    allw, dropped = [], 0
    for w in S.words(key):
        seg = w["seg"]
        if seg.get("compression_ratio", 0) > 2.6 or (seg.get("no_speech_prob", 0) > 0.6 and seg.get("avg_logprob", 0) < -0.8):
            dropped += 1; continue
        d, lvl = S.diff(w["s"], w["e"])
        stock = re.sub(r"[^a-z]", "", seg["text"].lower()) in STOCK
        if not w["n"] or lvl < floor + 3 or (stock and lvl < floor + 10):
            dropped += 1; continue
        w["d"] = d * sign                      # >0: this mic's wearer
        allw.append(w)
    own, gave = [], []
    for i, w in enumerate(allw):
        d = w["d"]
        if abs(d) < CONFIDENT_DB:              # marginal: lean on neighbours within ±1 s
            near = [x["d"] for x in allw[max(0, i - 4):i + 5] if abs(x["s"] - w["s"]) < 1.0]
            d = 0.5 * d + 0.5 * float(np.median(near))
        w["amb"] = abs(d) < 1.5
        w["spk"] = S.spk[key]
        (own if d > 0 else gave).append(w)
    return own, gave, dropped


A, gaveA, dropA = load("a")
B, gaveB, dropB = load("b")


def rescue(own, gave, other):
    """Quiet words at speaker changes can be given away by both tracks; keep them if the other lacks them."""
    have = {}
    for x in other:
        have.setdefault(x["n"], []).append(x["s"])
    n = 0
    for w in gave:
        if abs(w["d"]) < CONFIDENT_DB and w["d"] > 0 and not any(abs(t - w["s"]) < 1.0 for t in have.get(w["n"], [])):
            w["amb"] = True; own.append(w); n += 1
    own.sort(key=lambda x: x["s"])
    return n


rescued = rescue(A, gaveA, B) + rescue(B, gaveB, A)

# De-duplicate words both tracks kept in near-equal stretches.
byB = {}
for j, w in enumerate(B):
    byB.setdefault(w["n"], []).append(j)
dA, dB = set(), set()
for i, w in enumerate(A):
    if not w["amb"]:
        continue
    for j in byB.get(w["n"], []):
        if j in dB or abs(B[j]["s"] - w["s"]) > 1.0:
            continue
        if not B[j]["amb"]:
            dA.add(i)
        else:
            (dB.add(j) if w["d"] > 0 else dA.add(i))
        break
A = [w for i, w in enumerate(A) if i not in dA]
B = [w for j, w in enumerate(B) if j not in dB]


def utterances(words):
    out = []
    for w in words:
        if out and w["s"] - out[-1]["e"] < 1.2:
            out[-1]["w"].append(w); out[-1]["e"] = max(out[-1]["e"], w["e"])
        else:
            out.append(dict(spk=w["spk"], s=w["s"], e=w["e"], w=[w]))
    return out


utts = sorted(utterances(A) + utterances(B), key=lambda u: u["s"])

# Crosstalk: utterances from both people overlapping > 1 s where the mics are near-equal.
for u in utts:
    u["cross"] = False
for i, u in enumerate(utts):
    for v in utts[i + 1:i + 8]:
        if v["s"] > u["e"]:
            break
        if v["spk"] != u["spk"]:
            s0, s1 = max(u["s"], v["s"]), min(u["e"], v["e"])
            if s1 - s0 > 1.0 and abs(S.diff(s0, s1)[0]) < 3.0:
                u["cross"] = v["cross"] = True

NAME_FIXES = [(re.compile(rf"\b{re.escape(v)}\b"), k) for k, vs in S.cfg.get("spellings", {}).items() for v in vs]


def render(words):
    """Join words; runs of >=2 consecutive low-confidence words become [unclear: ...]."""
    out, run = [], []
    def flush():
        if len(run) >= 2:
            out.append("[unclear: " + " ".join(x["text"] for x in run) + "]")
        else:
            out.extend(x["text"] for x in run)
        run.clear()
    for w in words:
        (run.append(w) if w["p"] < 0.3 else (flush(), out.append(w["text"])))
    flush()
    txt = re.sub(r"\s+([,.?!;:])", r"\1", re.sub(r"\s+", " ", " ".join(out)).strip())
    for rx, good in NAME_FIXES:
        txt = rx.sub(good, txt)
    return txt


turns = []
for u in utts:
    txt = render(u["w"])
    if not txt:
        continue
    if u["cross"]:
        txt = "[crosstalk] " + txt
    if turns and turns[-1]["spk"] == u["spk"]:
        turns[-1]["text"] += " " + txt; turns[-1]["e"] = u["e"]
    else:
        turns.append(dict(spk=u["spk"], s=u["s"], e=u["e"], text=txt))

cues = []
for u in utts:
    cur = []
    for w in u["w"]:
        if cur and (w["e"] - cur[0]["s"] > 7 or len(" ".join(x["text"] for x in cur)) > 84):
            cues.append((cur[0]["s"], cur[-1]["e"], u["spk"], render(cur))); cur = []
        cur.append(w)
    if cur:
        cues.append((cur[0]["s"], cur[-1]["e"], u["spk"], render(cur)))

names = f"{S.spk['a']} & {S.spk['b']}"
write_outputs(args.outdir, turns, cues, dict(title=f"{args.title}: {names}", date=args.date,
              participants=f"{S.spk['a']}, {S.spk['b']}", total=S.total))
stats = dict(dropped_as_bleed_or_noise=[dropA, dropB], rescued=rescued, dedup_removed=len(dA) + len(dB),
             turns=len(turns), srt_cues=len(cues),
             unclear_marks=sum(t["text"].count("[unclear") for t in turns),
             crosstalk_marks=sum(t["text"].count("[crosstalk]") for t in turns),
             words={S.spk[k]: sum(len(u["w"]) for u in utts if u["spk"] == S.spk[k]) for k in "ab"},
             total=hms(S.total))
json.dump(turns, open(os.path.join(args.workdir, "turns.json"), "w"))
json.dump(stats, open(os.path.join(args.workdir, "merge_stats.json"), "w"), indent=1)
print(json.dumps(stats, indent=1))
