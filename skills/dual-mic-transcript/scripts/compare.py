"""Compare an app transcript (e.g. Wispr Flow) with the mic-only merge, to decide whether a hybrid is worth it.

usage: compare.py <workdir> <app_transcript.txt>

Reports word overlap, speaker-label quality of the app transcript, and how many app-only words were
actually heard by a mic (= real speech the merge dropped) vs. heard by neither (app guessed or caught more).
"""
import collections, difflib, json, os, re, sys
from common import Session, norm

S = Session(sys.argv[1])
raw = [l for l in open(sys.argv[2]) if l.strip()]
labels = collections.Counter(l.split(":", 1)[0].strip() for l in raw if ":" in l)
W = [norm(x) for l in raw for x in (l.split(":", 1)[1] if ":" in l else l).split() if norm(x)]
T = json.load(open(os.path.join(sys.argv[1], "turns.json")))
O, Ot = [], []
for t in T:
    ws = [norm(x) for x in re.sub(r"\[(unclear: |crosstalk\] ?)|\]", "", t["text"]).split() if norm(x)]
    O += ws; Ot += [t["s"] + (t["e"] - t["s"]) * i / max(1, len(ws)) for i in range(len(ws))]
R = {k: [(w["s"], w["n"]) for w in S.words(k) if w["n"]] for k in "ab"}

sm = difflib.SequenceMatcher(None, W, O, autojunk=False)
shared = sum(b.size for b in sm.get_matching_blocks())
print(f"app: {len(W)} words, labels {dict(labels.most_common(4))}")
print(f"mic-only merge: {len(O)} words")
print(f"shared: {shared} = {shared / len(W):.0%} of app, {shared / len(O):.0%} of merge")


def heard(t, words, key):
    c = collections.Counter(x for s, x in R[key] if abs(s - t) < 8)
    n = 0
    for w in words:
        if c[w] > 0:
            n += 1; c[w] -= 1
    return n


real = guessed = mine = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    t = Ot[min(j1, len(Ot) - 1)]
    if tag == "delete":
        ws = W[i1:i2]; h = max(heard(t, ws, "a"), heard(t, ws, "b"))
        real += h; guessed += len(ws) - h
    elif tag == "insert":
        mine += j2 - j1
print(f"app-only words heard by a mic (merge dropped real speech): {real}")
print(f"app-only words heard by neither mic (app caught more, guessed, or pre/post-roll): {guessed}")
print(f"merge-only words: {mine}")
top = labels.most_common(1)[0][1] / max(1, sum(labels.values())) if labels else 1
print("app speaker labels look " + ("UNUSABLE (one label on most lines)" if top > 0.8 else "usable") + f": top label on {top:.0%} of lines")
print("Recommendation:", "hybrid (app text + mic speakers/timestamps)" if real > 0.03 * len(O) else "mic-only merge is enough")
