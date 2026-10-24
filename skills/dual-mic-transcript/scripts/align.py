"""Find the offset between the two mics, check drift, calibrate levels, and check who wore which mic.

usage: align.py <workdir>

Reads a.wav / b.wav, writes envA.npy / envB.npy (10 ms RMS envelopes) and updates config.json with:
  offset_a, offset_b   seconds to add to each mic's own time to get session time (t=0 = earliest start)
  lags                 fine lag measured at points across the session (drift check)
  boundary_db          level ratio (A mic minus B mic, dB) halfway between the two speakers' clusters
  clusters_db          where each speaker's speech sits on that ratio
  pitch_hz             median voice pitch when each mic is clearly the louder one
"""
import json, os, sys, wave
import numpy as np

work = sys.argv[1]
cfg = json.load(open(os.path.join(work, "config.json")))
SR, HOP = 16000, 160


def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


A, B = load(os.path.join(work, "a.wav")), load(os.path.join(work, "b.wav"))


def env(x):
    n = len(x) // HOP; return np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(1) + 1e-12)


eA, eB = env(A), env(B)
np.save(os.path.join(work, "envA.npy"), eA); np.save(os.path.join(work, "envB.npy"), eB)


def xcorr(a, b, maxlag):
    a = a - a.mean(); b = b - b.mean(); n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
    c = np.fft.irfft(np.fft.rfft(a, n) * np.conj(np.fft.rfft(b, n)), n)
    cc = np.concatenate([c[-maxlag:], c[:maxlag + 1]]); i = int(np.argmax(cc))
    return i - maxlag, float(cc[i] / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


# Coarse: log envelopes over the first 20 min, ±120 s. lag>0: an event at A time t is at B time t-lag.
L = min(len(eA), len(eB), 120000)
lag_f, pk = xcorr(np.log(eA[:L]), np.log(eB[:L]), 12000)
coarse = lag_f * HOP
print(f"coarse lag {lag_f / 100:+.2f} s (corr {pk:.2f})")
if pk > 0.98:
    print("WARNING: the two tracks are nearly identical. One mic's files were probably copied into both folders.")

# Fine: raw audio, 60 s windows spread across the overlap
dur = min(len(A), len(B)) / SR
lags = []
for t0 in np.linspace(120, max(121, dur - 180), 13):
    t0 = int(t0); a = A[t0 * SR:(t0 + 60) * SR]; s = t0 * SR - coarse; b = B[s:s + 60 * SR]
    if s < 0 or len(b) < len(a):
        continue
    l, c = xcorr(a, b, 8000)
    lags.append({"t": t0, "lag_s": (coarse + l) / SR, "corr": round(c, 3)})
vals = np.array([x["lag_s"] for x in lags])
lag = float(np.median(vals))
print(f"fine lag median {lag:+.4f} s, spread {1000 * (vals.max() - vals.min()):.1f} ms over {len(vals)} points")
# B time = A time - lag. If lag < 0, B started first (B's t=0 happened before A's).
offset_a, offset_b = (-lag, 0.0) if lag < 0 else (0.0, lag)

# Level ratio on the session timeline
fa, fb = int(round(offset_a * 100)), int(round(offset_b * 100))
N = max(len(eA) + fa, len(eB) + fb)
PA = np.full(N, 1e-12); PA[fa:fa + len(eA)] = eA ** 2
PB = np.full(N, 1e-12); PB[fb:fb + len(eB)] = eB ** 2
dA, dB = 10 * np.log10(PA), 10 * np.log10(PB)
floor = max(np.percentile(dA, 10), np.percentile(dB, 10))
act = np.maximum(dA, dB) > floor + 12
r = (dA - dB)[act]
# Two-speaker Gaussian mixture on the ratio. The boundary is where a frame is equally likely to be
# either speaker. (A plain midpoint between the peaks is biased when one voice's spread is much wider,
# e.g. a quiet speaker whose bleed level varies a lot.)
mu, sd, pi = np.array([-6.0, 6.0]), np.array([3.0, 3.0]), np.array([0.5, 0.5])
for _ in range(200):
    p = pi * np.exp(-0.5 * ((r[:, None] - mu) / sd) ** 2) / sd
    g = p / (p.sum(1, keepdims=True) + 1e-300)
    pi = g.mean(0); mu = (g * r[:, None]).sum(0) / g.sum(0)
    sd = np.sqrt((g * (r[:, None] - mu) ** 2).sum(0) / g.sum(0)) + 1e-6
xs = np.linspace(mu.min(), mu.max(), 4000)
post = pi * np.exp(-0.5 * ((xs[:, None] - mu) / sd) ** 2) / sd
boundary = float(xs[np.argmin(abs(post[:, 0] - post[:, 1]))])
mB, mA = float(mu.min()), float(mu.max())
print(f"level clusters: mic-A speaker {mA:+.1f} dB, mic-B speaker {mB:+.1f} dB -> boundary {boundary:+.1f} dB")
if mA - mB < 6:
    print("WARNING: weak level separation between the speakers; speaker labels will be less reliable.")


def f0(x):
    x = x - x.mean()
    if np.sqrt((x * x).mean()) < 1e-3:
        return None
    c = np.correlate(x, x, "full")[len(x) - 1:]; lo, hi = SR // 400, SR // 70
    k = lo + int(np.argmax(c[lo:hi])); return SR / k if c[k] > 0.5 * c[0] else None


rng = np.random.default_rng(0)
pitch = {}
for key, mask, sig, off in (("a", (dA - dB > boundary + 5) & (np.maximum(dA, dB) > floor + 12), A, offset_a),
                            ("b", (dA - dB < boundary - 5) & (np.maximum(dA, dB) > floor + 12), B, offset_b)):
    idx = np.flatnonzero(mask); fs = []
    for i in rng.choice(idx, min(3000, len(idx)), replace=False) if len(idx) else []:
        s = int((i / 100 - off) * SR); v = f0(sig[s:s + 640]) if s >= 0 else None
        if v:
            fs.append(v)
    pitch[key] = float(np.median(fs)) if fs else None
for key in ("a", "b"):
    p = pitch[key]
    kind = "unknown" if p is None else "lower (typically male)" if p < 165 else "higher (typically female)"
    print(f"mic {key} ({cfg['mics'][key]['speaker']}): wearer's median pitch {p and round(p)} Hz, {kind}")
print("Check those against who you expect wore each mic; if they're reversed, the mics were swapped.")

cfg.update(offset_a=offset_a, offset_b=offset_b, lags=lags, boundary_db=boundary,
           clusters_db={"a": mA, "b": mB}, pitch_hz=pitch, floor_db=float(floor), session_s=N / 100)
json.dump(cfg, open(os.path.join(work, "config.json"), "w"), indent=1)
