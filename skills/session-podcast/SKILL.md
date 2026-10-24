---
name: session-podcast
description: Render, or re-render after edits, a two-host recap podcast MP3 from a dialogue script, locally with Kokoro-82M TTS. It parses a hand-editable script.md (**Alex:** … / **Jordan:** …), assigns a voice per host, normalizes loudness, and writes a player-safe MP3. Use when the user edits a podcast script and wants new audio, wants different voices or pacing, or has a new script from session-learning-kit.
---

# Session Podcast

## Files
```text
<client>/podcast/
  script.md          source of truth for edits: "**Alex:** text" paragraphs, blank line between
  script.json        machine copy; rewritten from script.md on every render
  session-recap.mp3  output (44.1 kHz stereo, -16 LUFS, written atomically)
```
A paragraph without a `**Name:**` prefix continues the previous speaker. Headings (`# …`) are ignored.

## Re-render after editing the script
```bash
KOKORO_PY=~/code/atxworkshop/.venv/bin/python     # or the venv from scripts/setup.sh
$KOKORO_PY scripts/render.py <client>/podcast/script.md <client>/podcast/session-recap.mp3
```
- ~1 min of compute per ~5 min of audio on an M4 Max.
- **Always render from `script.md`** so the user's edits win.
- Before overwriting an MP3 the user may want to keep, copy it to `session-recap.prev.mp3`.

Options:
- `--voice ALEX=af_heart --voice JORDAN=am_michael`: defaults shown. Add one per extra speaker name.
  - Other American voices: `af_bella`, `af_nicole`, `af_sarah`, `am_adam`, `am_fenrir`, `am_puck`.
  - British (`bf_*`, `bm_*`) need `lang_code="b"`.
- `--speed 1.05` for slightly faster delivery; `--gap 0.5` for more space between speakers.

## Writing tips for scripts that sound good
- Short sentences; contractions; one idea per line.
- Spell things as they should be spoken: "M-C-P", "skills dot S-H", "Opus five point five".
- No stage directions, sound effects, markdown or timestamps. `render.py` strips `[HH:MM:SS]`, but nothing else.
- To change emphasis, rephrase. Kokoro has no SSML.

## Verify before saying it's done
```bash
ffprobe -v error -show_entries stream=sample_rate,channels:format=duration -of compact out.mp3
ffmpeg -nostdin -hide_banner -i out.mp3 -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
```
- Expect a mean around −17 to −21 dB and a max near −2 to −5 dB.
- For an objective check that it's speech, transcribe a 20 s clip with whisper `base`.
- If the user hears silence but the levels are fine, they likely opened it mid-write (older renders weren't atomic) or their player choked on the format. Re-render; output is now stereo 44.1 kHz.

## First-time setup
Run `scripts/setup.sh [venv]`. It installs ffmpeg, espeak-ng, a Python 3.10–3.12 venv with `kokoro` and `soundfile`, and pre-downloads the model.

No script yet? Write one with `session-learning-kit` (`--steps podcast`).
