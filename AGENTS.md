# Agent Skills

This repo is a skill library, not one giant prompt. Each directory in `skills/` is an independent skill. Install or symlink those directories; do not install `context/`.

## Choose the narrowest skill

Interview:

- Role drills, scoring, product accuracy, flashcards from mock answers: `technical-client-facing-interview-coach`
- Career evidence, story library, competency maps, retrieval cards: `sa-interview-story-coach`

Learning:

- New product or concept: `concept-tutor`
- A real repo, file, or request path: `codebase-xray`
- One architecture curveball or objection: `architecture-sparring`
- Review, gaps, flashcards, study plan: `learning-consolidator`

Session content (client coaching sessions):

- Two per-person mic recordings → speaker-labeled transcript: `dual-mic-transcript`
- Transcript → study guide, flashcards, quiz, podcast script: `session-learning-kit`
- Edited podcast script → new MP3: `session-podcast`
- Client session audio and text stay local by default; ask before using any cloud model.

Workflow:

- Pass work to a fresh agent, or write or audit HANDOFF.md: `handoff`

ATX Workshops operations (draft only; the owner sends):

- Reply to a prospect about a workshop or offer: `value-first-customer-reply`
- Stripe payment arrived: `atxworkshops-payment-confirm`
- Paid in-person session booked: `in-person-client-session-setup`
- Deck final, build client Docs: `client-workshop-artifacts`

Combine skills only when the request needs more than one mode. Do not activate every skill by default.

## Pedagogy

- Start top down: customer problem, mental model, mechanism, what it looks like in production, trade-offs.
- Separate what docs say, what code shows, and what you recommend.
- Do not invent APIs, metrics, customer names, or outcomes.
- For drills, ask one question and wait. Score the first pass separately from recovery after hints.
- If `context/learner-profile.md` or `learner-profile.md` exists, use it. Do not assume it is global.
- `context/curriculum/` is an optional study map, not a source of current product facts.

## Refining skills in this repo

- Keep `name` in `SKILL.md` identical to the skill directory name.
- Edit only the skill that owns the behavior. Shared study notes belong in `context/`, not inside a skill.
- Put long material in `references/`, sample interactions in `examples/`, and output formats in `templates/`.
- Do not add agent attribution to commit messages. Do not push unless asked.
