# Agent Skills

Portable skills for customer-facing technical interview prep and technical learning. Each skill is one folder with a `SKILL.md`. Agents load a skill by that file; they should not treat this whole repo as a single prompt.

Remote: https://github.com/juantmoore/skills

## Layout

```text
skills/     installable skills (one directory per skill)
context/    local study context; not part of a skill
scripts/    symlink skills into agent skill directories
```

`context/` holds an example learner profile, a Vercel SA curriculum, and a learning-log template. Edit those for a person or project. Do not copy them into every skill.

## Skills

### Interview

| Skill | Use when |
| --- | --- |
| `technical-client-facing-interview-coach` | Mock SA / SE / TAM / FDE / DevRel interviews, scoring, and study cards |
| `sa-interview-story-coach` | Turning real experience into evidence-backed stories, maps, and retrieval cards |

### Learning

| Skill | Use when |
| --- | --- |
| `concept-tutor` | Teaching a product or concept from first principles |
| `codebase-xray` | Tracing how a concept actually works in a repo |
| `architecture-sparring` | One-question architecture curveballs and objections |
| `learning-consolidator` | Grading practice and writing only the cards you need |

### Session content (coaching / workshops)

| Skill | Use when |
| --- | --- |
| `dual-mic-transcript` | Two lav-mic recordings (one per person) → one speaker-labeled, timestamped transcript, locally; optional hybrid with a Wispr Flow / Otter transcript |
| `session-learning-kit` | Transcript → study guide, flashcards (Anki), quiz, and podcast script on a local LLM |
| `session-podcast` | Render or re-render a two-host podcast MP3 from an (edited) script with Kokoro TTS |

These three run as a chain: transcript → learning kit → podcast. Each has a `scripts/` folder; all processing is local.

### Workflow

| Skill | Use when |
| --- | --- |
| `handoff` | Passing work to a fresh agent: write or audit `HANDOFF.md` against a 10-section checklist, then produce a kickoff prompt (`/handoff` in Claude Code) |

### ATX Workshops operations (from grok-bot)

| Skill | Use when |
| --- | --- |
| `value-first-customer-reply` | Replying to a prospect about a workshop or service: lead with outcomes, book a discovery call; price comes in the proposal |
| `atxworkshops-payment-confirm` | A Stripe payment arrives: draft the confirmation email and calendar holds for the owner to send |
| `in-person-client-session-setup` | A paid in-person session is booked: client folder, invite, Know Before You Go guide, readiness checklist, recording and delivery |
| `client-workshop-artifacts` | The workshop deck is final: build the client's Business Context report and agent instruction Docs |

These follow the Customer Workshop Playbook and only draft client email; the owner reviews and sends.

## Use with other agents

Link this repo so edits here show up everywhere:

```bash
./scripts/link-skills.sh
```

With no arguments that links every skill into:

- `~/.agents/skills` (OpenCode and other agent runtimes)
- `~/.codex/skills` (Codex)
- `~/.claude/skills` (Claude Code)

Pass explicit directories if you only want some of them:

```bash
./scripts/link-skills.sh ~/.agents/skills
```

Or copy once:

```bash
cp -R skills/* ~/.agents/skills/
```

Invoke by the directory name, for example `sa-interview-story-coach` or `concept-tutor`. Read `AGENTS.md` for which skill to pick.

## Refine

Change behavior in that skill's `SKILL.md`. Keep long reference material in `references/`, samples in `examples/`, and output formats in `templates/`. The `name` in frontmatter must match the folder name.
