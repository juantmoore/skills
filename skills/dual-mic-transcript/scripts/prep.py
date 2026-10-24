"""Concatenate each mic's recordings into one 16 kHz mono WAV and start the run config.

usage: prep.py <workdir> --a NAME FILE... --b NAME FILE...

Files for each mic are sorted by name (Rode splits long takes into numbered files, each one
starting where the previous ended). Writes <workdir>/a.wav, b.wav and config.json.
"""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("workdir")
ap.add_argument("--a", nargs="+", required=True, help="speaker name for mic A, then its files")
ap.add_argument("--b", nargs="+", required=True, help="speaker name for mic B, then its files")
args = ap.parse_args()
os.makedirs(args.workdir, exist_ok=True)


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


cfg = {"mics": {}}
for key, spec in (("a", args.a), ("b", args.b)):
    name, files = spec[0], sorted(spec[1:])
    if not files:
        sys.exit(f"mic {key}: no files given")
    durs = [dur(f) for f in files]
    offs = [sum(durs[:i]) for i in range(len(durs))]
    inputs = sum((["-i", f] for f in files), [])
    chain = "".join(f"[{i}:a]" for i in range(len(files))) + f"concat=n={len(files)}:v=0:a=1,aresample=16000:filter_size=64"
    out = os.path.join(args.workdir, f"{key}.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", chain,
                    "-ac", "1", "-c:a", "pcm_s16le", out], check=True)
    cfg["mics"][key] = {"speaker": name, "files": [os.path.abspath(f) for f in files], "durations": durs,
                        "file_offsets": offs, "total": sum(durs), "wav": out}
    print(f"mic {key} ({name}): {len(files)} files, {sum(durs) / 60:.1f} min -> {out}")
json.dump(cfg, open(os.path.join(args.workdir, "config.json"), "w"), indent=1)
