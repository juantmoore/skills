"""Generate a study guide, flashcards + quiz, and a podcast script from a session transcript.

Runs entirely against a local OpenAI-compatible server (LM Studio by default); nothing leaves the machine.

usage: make_content.py <transcript.md> <client_dir> --coach NAME --client NAME --date "October 23, 2026"
                       [--steps study flash podcast] [--model ID] [--base-url URL] [--cards 40] [--quiz 10]
                       [--minutes 12]

Writes <client_dir>/study-guide/, flashcards/, podcast/ (script.json + script.md). Render the podcast
audio with the session-podcast skill.
"""
import argparse, csv, json, re, sys, time
from pathlib import Path
from openai import OpenAI

ap = argparse.ArgumentParser()
ap.add_argument("transcript"); ap.add_argument("client_dir")
ap.add_argument("--coach", required=True); ap.add_argument("--client", required=True)
ap.add_argument("--date", required=True)
ap.add_argument("--steps", nargs="+", default=["study", "flash", "podcast"], choices=["study", "flash", "podcast"])
ap.add_argument("--model", default="qwen_qwen3.6-35b-a3b")
ap.add_argument("--base-url", default="http://localhost:1234/v1")
ap.add_argument("--cards", type=int, default=40); ap.add_argument("--quiz", type=int, default=10)
ap.add_argument("--minutes", type=int, default=12)
a = ap.parse_args()

llm = OpenAI(base_url=a.base_url, api_key="local")
out_dir = Path(a.client_dir)
transcript = Path(a.transcript).read_text()
coach, learner = a.coach, a.client

SYSTEM = (
    "You turn recorded coaching sessions into learning material for the client. "
    f"{coach} is the coach; {learner} is the client learning from them. "
    "Use only what is actually said in the transcript. Do not invent facts, tools, or advice. "
    "Where the transcript says [unclear] or [crosstalk], do not guess what was said. "
    "Cite timestamps in [HH:MM:SS] form copied from the transcript."
)


def ask(prompt, max_tokens=12000):
    t = time.time()
    r = llm.chat.completions.create(
        model=a.model, temperature=0.4, max_tokens=max_tokens,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": f"<transcript>\n{transcript}\n</transcript>\n\n{prompt}"}])
    out = re.sub(r"<think>.*?</think>", "", r.choices[0].message.content or "", flags=re.S).strip()
    print(f"  {len(out)} chars in {time.time() - t:.0f}s", file=sys.stderr)
    return out


def json_block(text, opener):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    closer = "]" if opener == "[" else "}"
    return json.loads(m.group(1) if m else text[text.find(opener):text.rfind(closer) + 1])


if "study" in a.steps:
    print("study guide…", file=sys.stderr)
    guide = ask(f"""Write a study guide for {learner} in Markdown. Sections, in this order:

# Session Study Guide (title line, then the date {a.date}, and participants)
## The big picture: 4–6 sentences on what this session covered and why it matters for them
## Chapters: 6–12 chapters in time order. For each: a heading with its start [HH:MM:SS], 2–4 bullet points of the key ideas, and one "In {coach}'s words" short quote copied verbatim from the transcript
## Key concepts: each concept in plain language, 1–3 sentences, with the [HH:MM:SS] where it came up
## Glossary: alphabetical terms (tools, model names, jargon) with one-line definitions as they were explained in the session
## {learner}'s questions: the questions they asked, each with a one-line summary of {coach}'s answer and the timestamp
## Action items & homework: concrete next steps that were agreed or suggested
## Open questions: things left unresolved or worth revisiting next session

Be specific to this conversation, not generic advice.""")
    # The model sometimes copies the section instructions into the headings ("## Chapters: 6–12 chapters…").
    guide = re.sub(r"^(## [^:\n]+):.*$", r"\1", guide, flags=re.M)
    d = out_dir / "study-guide"; d.mkdir(parents=True, exist_ok=True)
    (d / "study-guide.md").write_text(guide + "\n")

if "flash" in a.steps:
    print("flashcards…", file=sys.stderr)
    data = json_block(ask(f"""Create {a.cards} flashcards and a {a.quiz}-question quiz that help {learner} remember this session.
Return ONLY a JSON object in a ```json code block, shaped:
{{"cards": [{{"front": "...", "back": "...", "timestamp": "HH:MM:SS", "tag": "short-topic"}}],
 "quiz": [{{"question": "...", "choices": ["A ...", "B ...", "C ...", "D ..."], "answer": "B", "explanation": "...", "timestamp": "HH:MM:SS"}}]}}
Cards: one idea each, front is a question, back is a 1–2 sentence answer grounded in what {coach} said.
Mix recall ("What is…"), application ("When would you use…"), and comparison cards.""", max_tokens=16000), "{")
    d = out_dir / "flashcards"; d.mkdir(parents=True, exist_ok=True)
    (d / "flashcards.json").write_text(json.dumps(data, indent=2) + "\n")
    with open(d / "anki-import.tsv", "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        for c in data["cards"]:
            w.writerow([c["front"], f'{c["back"]}<br><small>Session @ {c["timestamp"]}</small>', c.get("tag", "")])
    title = f"Session with {coach}, {a.date}"
    md = [f"# Flashcards: {title}\n"] + [f"**{i}. {c['front']}**  \n{c['back']} *([{c['timestamp']}])*\n"
                                         for i, c in enumerate(data["cards"], 1)]
    (d / "flashcards.md").write_text("\n".join(md))
    qz, key = [f"# Quiz: {title}\n"], ["\n---\n\n## Answer key\n"]
    for i, q in enumerate(data["quiz"], 1):
        qz.append(f"**{i}. {q['question']}**\n\n" + "\n".join(f"- {c}" for c in q["choices"]) + "\n")
        key.append(f"{i}. **{q['answer']}**: {q['explanation']} *([{q['timestamp']}])*")
    (d / "quiz.md").write_text("\n".join(qz + key) + "\n")

if "podcast" in a.steps:
    print("podcast script…", file=sys.stderr)
    words = a.minutes * 150
    lines = json_block(ask(f"""Write a script for a two-host recap podcast episode (about {a.minutes} minutes spoken, roughly {words - 100}–{words + 100} words) made for {learner} to listen to as review.
Hosts: ALEX (curious, asks the questions a learner would) and JORDAN (explains clearly, uses {coach}'s examples). They are recap hosts, not {coach} or {learner}; they refer to "{coach}" and "{learner}" by name.
Structure: a warm cold open; 4–6 segments covering the session's most important ideas in order, each with a concrete example from the session; a "quick quiz" segment where Alex asks 3 questions and pauses before Jordan answers; a wrap-up with their action items.
Style: natural spoken English, short sentences, contractions, occasional light humor, no stage directions, no sound effects, no markdown, no timestamps in the dialogue. Spell out numbers and acronyms the way they should be spoken when helpful.
Return ONLY a JSON array in a ```json code block: [{{"speaker": "ALEX", "text": "..."}}, {{"speaker": "JORDAN", "text": "..."}}, ...]""", max_tokens=16000), "[")
    for l in lines:   # timestamps would be read aloud by the TTS
        l["text"] = re.sub(r"\s+", " ", re.sub(r"\s*\[\d{1,2}:\d{2}:\d{2}\]", "", l["text"])).strip()
    d = out_dir / "podcast"; d.mkdir(parents=True, exist_ok=True)
    (d / "script.json").write_text(json.dumps(lines, indent=2) + "\n")
    (d / "script.md").write_text("# Podcast script: Session recap\n\n" +
                                 "\n\n".join(f"**{l['speaker'].title()}:** {l['text']}" for l in lines) + "\n")
