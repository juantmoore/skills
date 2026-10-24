"""Render a two-host podcast script to an MP3 locally with Kokoro-82M.

usage: render.py <script.md|script.json> <out.mp3> [--voice ALEX=af_heart --voice JORDAN=am_michael]
                 [--speed 1.0] [--gap 0.35]

script.md format (what make_content.py writes, and what you edit by hand):
    **Alex:** line of dialogue
    (blank line)
    **Jordan:** next line
A paragraph without a "**Name:**" prefix continues the previous speaker. Rendering from script.md
also rewrites script.json next to it, so the two stay in sync.

The MP3 is 44.1 kHz stereo, loudness-normalized to -16 LUFS, and only moved into place once complete.
"""
import argparse, json, os, re, subprocess, sys, tempfile
import numpy as np, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("script"); ap.add_argument("out")
ap.add_argument("--voice", action="append", default=[], help="SPEAKER=kokoro_voice, e.g. ALEX=af_heart")
ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--gap", type=float, default=0.35, help="seconds of silence between speakers")
a = ap.parse_args()

VOICES = {"ALEX": "af_heart", "JORDAN": "am_michael"}
VOICES.update({k.upper(): v for k, v in (x.split("=", 1) for x in a.voice)})
SR = 24000


def parse_md(path):
    lines = []
    for para in re.split(r"\n\s*\n", open(path).read()):
        para = " ".join(para.split())
        if not para or para.startswith("#"):
            continue
        m = re.match(r"^\*\*([^*:]+):\*\*\s*(.*)$", para)
        if m:
            lines.append({"speaker": m.group(1).strip().upper(), "text": m.group(2).strip()})
        elif lines:
            lines[-1]["text"] += " " + para
    return lines


if a.script.endswith(".md"):
    script = parse_md(a.script)
    json.dump(script, open(os.path.join(os.path.dirname(os.path.abspath(a.script)), "script.json"), "w"), indent=2)
else:
    script = json.load(open(a.script))
if not script:
    sys.exit("no dialogue found; expected paragraphs like '**Alex:** text'")
unknown = sorted({l["speaker"].upper() for l in script} - VOICES.keys())
if unknown:
    sys.exit(f"no voice for {unknown}; pass e.g. --voice {unknown[0]}=af_bella")
# Timestamps like [00:12:34] would be read aloud.
for l in script:
    l["text"] = re.sub(r"\s+", " ", re.sub(r"\s*\[\d{1,2}:\d{2}:\d{2}\]", "", l["text"])).strip()

from kokoro import KPipeline   # imported late so argument errors are instant
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
chunks = [np.zeros(int(SR * 0.5), dtype=np.float32)]
for i, line in enumerate(script):
    for _, _, audio in pipe(line["text"], voice=VOICES[line["speaker"].upper()], speed=a.speed):
        chunks += [audio.numpy(), np.zeros(int(SR * 0.12), dtype=np.float32)]
    chunks.append(np.zeros(int(SR * a.gap), dtype=np.float32))
    print(f"\r{i + 1}/{len(script)}", end="", file=sys.stderr)
audio = np.concatenate(chunks)

part = a.out + ".part.mp3"
with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
    sf.write(tmp.name, audio, SR)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", tmp.name,
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2",
                    "-c:a", "libmp3lame", "-b:a", "160k", part], check=True)
os.replace(part, a.out)
print(f"\nwrote {a.out} ({len(audio) / SR / 60:.1f} min, {len(script)} lines)", file=sys.stderr)
