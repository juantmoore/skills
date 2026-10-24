---
name: session-learning-kit
description: Turn a coaching or working-session transcript into learning material for the client: a study guide with timestamped chapters, flashcards (Anki import), a quiz, and a two-host recap podcast script. It runs on a local LLM (LM Studio) so client content stays private. Use after a session transcript exists and the user wants review or reinforcement material, or wants to regenerate it after the transcript changes.
---

# Session Learning Kit

Input: a speaker-labeled transcript with `[HH:MM:SS]` timestamps, e.g. from `dual-mic-transcript`.

Output, grouped per client or project:
```text
<content-root>/<client-slug>/
  study-guide/study-guide.md     big picture, chapters (timestamped, with verbatim quotes), key concepts,
                                 glossary, the client's questions, action items, open questions
  flashcards/flashcards.md       N cards with timestamps; anki-import.tsv (front, back, tag); flashcards.json
  flashcards/quiz.md             multiple choice + answer key with timestamps
  podcast/script.md, script.json two-host recap script (render audio with `session-podcast`)
```

## Privacy default
Client sessions stay on the machine: use the local model.
- Only use a cloud model (Venice, frontier APIs) if the user says so, and suggest they get the client's OK first.
- A full 2.5 h transcript is ~35k tokens, so a frontier polish pass costs cents if they choose it.

## Run
1. Start the local model, with enough context for the whole transcript:
   ```bash
   ~/.lmstudio/bin/lms server start
   ~/.lmstudio/bin/lms load qwen_qwen3.6-35b-a3b --context-length 65536 --gpu max -y
   ```
   Any OpenAI-compatible local server works (`--base-url`, `--model`). On a 64 GB M4 Max, Qwen3.6-35B-A3B takes ~21 GB and writes each piece in 1.5–2.5 min.
2. Generate (needs a Python with the `openai` package; on this machine `~/code/atxworkshop/.venv`):
   ```bash
   python scripts/make_content.py transcript.md <content-root>/<client-slug> \
       --coach Patrick --client Sam --date "October 23, 2026" [--steps study flash podcast] \
       [--cards 40 --quiz 10 --minutes 12]
   ```
   `--steps podcast` regenerates only the script, and so on.
3. **Review before delivering.** Read the study guide's chapters and a sample of the cards against the transcript:
   - quotes must be verbatim
   - timestamps must exist
   - nothing invented
   The script already strips instruction text the model copies into headings, and `[HH:MM:SS]` from podcast dialogue.
4. Render the podcast with `session-podcast`.

## Regenerating
- If the transcript improves (say, a hybrid replaces the mic-only one), copy the current outputs to `<client-slug>/.previous/` first, then regenerate all steps. Content inherits the transcript's gaps.
- The user may hand-edit `podcast/script.md`. **Never regenerate the podcast script over manual edits without asking**; just re-render the audio.

## Pedagogy notes
- Retrieval practice (cards, quiz) is the highest-value piece; the study guide is the reference; the podcast is for passive review.
- Ground every card in what the coach actually said, and link back to the moment ("you asked this at 00:42:10").
- More ideas (client portal site via v0, spaced follow-up emails, cheat-sheet visuals): `references/content-ideas.md`.
