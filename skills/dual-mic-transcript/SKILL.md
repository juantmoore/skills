---
name: dual-mic-transcript
description: Turn a two-person session recorded on two lav mics (one per person, e.g. Rode Wireless PRO / GO) into one speaker-labeled, timestamped transcript, entirely on the local Mac. It aligns the mics, transcribes with local whisper, assigns speakers from mic levels, removes bleed, and optionally merges in an app transcript (Wispr Flow, Otter, Meet) for better wording. Use when the user has per-person mic recordings and wants a transcript, or wants to check or improve an app transcript against the mic audio.
---

# Dual-Mic Transcript

Each person wears their own mic, so **whoever's mic is louder is the one speaking**. Each mic also hears the other person ~5–9 dB quieter ("bleed"), so whisper transcribes *both* voices on *both* tracks. The pipeline keeps each word once, from its speaker's own mic.

Everything runs locally. Do not upload audio or transcript text to any API unless the user explicitly asks.

## 0. Find the tools (don't install first)
Check for an existing install before installing anything; see `references/local-tools.md`. Known-good here:
- `openai-whisper` + `~/.cache/whisper/large-v3-turbo.pt`, on **CPU**. Its word timestamps crash on Apple MPS (no float64).
- ffmpeg, numpy.
- Fallback for speed on Apple Silicon: `pip install mlx-whisper` with `mlx-community/whisper-large-v3-turbo`.

## 1. Inventory and check the files
- List each folder with ffprobe: duration, sample rate, birth/mtime.
- Rode transmitters split long takes into numbered files that are back to back. Their clocks are often unset (dates in 2000), so **don't trust start times**.
- **Checksum both folders** (`md5 -q`). Identical files mean one mic was copied twice. Stop and ask for the other mic's files: they're often still on the second transmitter, which may use a different naming scheme (`REC000xx.WAV` vs `000xx_Wireless_PRO.WAV`).

## 2. Prep and align
```bash
SK=<this skill>/scripts; W=<scratch workdir>
python3 $SK/prep.py  $W --a Patrick coach-mic/*.WAV --b Sam client-mic/*.WAV
python3 $SK/align.py $W
```
`align.py` measures:
- the **offset**, by cross-correlation at 13 points; the spread is your **drift** check
- the **speaker boundary**, from a two-speaker Gaussian fit on the mic-level ratio
- each mic's wearer **pitch**

**If the pitch contradicts the names** (a ~150 Hz voice on the woman's mic), the mics were swapped. Confirm by content: who asks vs. explains, and things like "this is Patrick's mic". Then rerun `prep.py` with the names swapped. Report the offset, drift and pitch to the user.

## 3. Transcribe (both mics in parallel, ~25 min for 2.5 h on an M4 Max)
```bash
python3 $SK/transcribe.py $W/a.wav $W/a.json 8 large-v3-turbo Patrick Sam &
python3 $SK/transcribe.py $W/b.wav $W/b.json 8 large-v3-turbo Patrick Sam &
wait
```
When waiting in a loop, use `pgrep -f "transcrib[e].py"`. A bare pattern matches the waiting shell itself and never exits.

## 4. Merge (mic-only transcript)
```bash
python3 $SK/merge.py  $W <outdir> --title "Working session" --date "October 23, 2026"
python3 $SK/verify.py $W <outdir>
```
How it works:
- Per-word level difference, smoothed by neighbours when marginal.
- Each speaker's words come from their own track only.
- A rescue pass catches quiet words at speaker changes.
- `[unclear: …]` marks runs of low-confidence words; `[crosstalk]` marks overlap with near-equal levels.

## 5. Optional: hybrid with an app transcript
If the user has a Wispr Flow / Otter / Meet transcript, run `compare.py $W app.txt` first.
- App transcripts usually have **better wording but useless speaker labels and no timestamps**.
- If `compare.py` recommends a hybrid:
```bash
python3 $SK/hybrid.py $W <outdir> app.txt --fixes fixes.json --title ... --date ... \
        --participants "Patrick, Sam (client, Acme Labs)" --source-name "Wispr Flow"
python3 $SK/verify.py $W <outdir> --hybrid     # expect >97% speaker agreement with the merge
```
- `fixes.json`: a list of `[regex, replacement]` for recurring mis-hearings (names, products). See `examples/fixes-example.json`.
- Only fix spellings you're sure of; list the rest as uncertain in notes.

## 6. Check the speaker boundary (important)
`align.py`'s fitted boundary is a good default, not gospel.
- Spot-check 15–25 short and long lines at random against content: the coach explains, the client asks.
- If teaching lines land on the client (or the reverse), set `"boundary_override_db": <value>` in `config.json` and rerun merge/hybrid. On the Oct 23 2026 session, 0.0 dB beat the fitted +0.5 dB on long lines.
- To compare two runs, diff which sentences changed speaker and judge them by content.

## 7. Deliver
Write `transcript.md` / `.txt` / `.srt` (the scripts do), then `notes.md` with:
- tool, model and settings
- the file→speaker mapping (and any swap)
- offset and drift
- boundary used
- gaps (`verify.py` lists silences > 45 s)
- `[unclear]` / `[crosstalk]` counts
- text fixes
- judgment calls

Template: `templates/notes.md`. Show the user the first 40 turns and a stretch from the middle before calling it done.

## Pitfalls seen in practice
- Labels by folder name were wrong: the files in the coach's folder were from the mic the client wore.
- Frame-level ownership with a high activity threshold drops soft speech. Use per-word decisions.
- Word-by-word ownership without neighbour smoothing flips single words mid-sentence.
- App transcripts can start before the mics (keep as an unverified preface) and stop before them (fill the tail from the merge).
