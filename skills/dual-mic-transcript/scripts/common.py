"""Shared helpers: session timeline, mic levels, output writers."""
import json, os, re
import numpy as np

FPS = 100


class Session:
    """Both mics' 10 ms power on one session timeline (from align.py's config)."""

    def __init__(self, work):
        self.work = work
        self.cfg = json.load(open(os.path.join(work, "config.json")))
        c = self.cfg
        self.spk = {"a": c["mics"]["a"]["speaker"], "b": c["mics"]["b"]["speaker"]}
        self.off = {"a": c["offset_a"], "b": c["offset_b"]}
        self.boundary = c.get("boundary_override_db", c["boundary_db"])
        eA, eB = np.load(os.path.join(work, "envA.npy")), np.load(os.path.join(work, "envB.npy"))
        fa, fb = int(round(self.off["a"] * FPS)), int(round(self.off["b"] * FPS))
        self.N = max(len(eA) + fa, len(eB) + fb)
        self.pA = np.full(self.N, 1e-12); self.pA[fa:fa + len(eA)] = eA ** 2
        self.pB = np.full(self.N, 1e-12); self.pB[fb:fb + len(eB)] = eB ** 2
        self.total = self.N / FPS

    def diff(self, s, e):
        """Mic-A minus mic-B level over [s, e] (session seconds), relative to the speaker boundary.
        >0: mic A's wearer, <0: mic B's wearer. Also returns the louder mic's level in dB."""
        a, b = int(s * FPS), max(int(s * FPS) + 1, int(e * FPS))
        a, b = max(0, min(a, self.N - 1)), max(1, min(b, self.N))
        qa, qb = self.pA[a:b].mean(), self.pB[a:b].mean()
        return 10 * np.log10(qa / qb) - self.boundary, 10 * np.log10(max(qa, qb))

    def floor(self):
        return float(np.percentile(10 * np.log10(np.maximum(self.pA, self.pB)), 10))

    def words(self, key):
        """Raw whisper words of one mic, on the session timeline."""
        out = []
        for seg in json.load(open(os.path.join(self.work, f"{key}.json")))["segments"]:
            for w in seg.get("words", []):
                out.append(dict(seg=seg, text=w["word"].strip(), n=norm(w["word"]), p=w.get("probability", 1.0),
                                s=w["start"] + self.off[key], e=max(w["end"], w["start"] + 0.05) + self.off[key]))
        return out


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def hms(t):
    t = max(0, int(t)); return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def srt_ts(t):
    ms = int(round(max(t, 0) * 1000))
    return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"


def write_outputs(outdir, turns, cues, meta, preface=None):
    """turns: [{spk, s, e, text}]; cues: [(start, end, spk, text)]; meta: title/date/participants/total/source."""
    os.makedirs(outdir, exist_ok=True)
    lines = [f"- **Date:** {meta['date']}", f"- **Participants:** {meta['participants']}",
             f"- **Total length:** {hms(meta['total'])}"] + [f"- **{k}:** {v}" for k, v in meta.get("extra", {}).items()]
    with open(os.path.join(outdir, "transcript.md"), "w") as f:
        f.write(f"# {meta['title']}\n\n" + "\n".join(lines) + "\n\n---\n\n")
        if preface:
            f.write(f"*{preface[0]}:* {preface[1]}\n\n---\n\n")
        for t in turns:
            f.write(f"**{t['spk']}** [{hms(t['s'])}]\n{t['text']}\n\n")
    with open(os.path.join(outdir, "transcript.txt"), "w") as f:
        f.write(meta["title"] + "\n" + "\n".join(re.sub(r"[*]", "", l).lstrip("- ") for l in lines) + "\n\n")
        if preface:
            f.write(f"{preface[0]}: {preface[1]}\n\n")
        for t in turns:
            f.write(f"{t['spk']} [{hms(t['s'])}]\n{t['text']}\n\n")
    with open(os.path.join(outdir, "transcript.srt"), "w") as f:
        for i, (s, e, spk, txt) in enumerate(sorted(cues, key=lambda c: c[0]), 1):
            f.write(f"{i}\n{srt_ts(s)} --> {srt_ts(max(e, s + 0.4))}\n{spk}: {txt}\n\n")
