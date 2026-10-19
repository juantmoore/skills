# Technical Client-Facing Interview Coach Skill

A reusable skill package for preparing candidates for Solutions Architect,
Solutions Engineer, Technical Account Manager, Forward Deployed Engineer, Developer
Relations, and similar customer-facing technical interviews.

## Files

- `SKILL.md` — main behavior and workflow
- `references/question-taxonomy.md` — scenario generation framework
- `references/scoring-rubric.md` — consistent answer evaluation
- `templates/flashcard-template.md` — compact study-card format
- `templates/session-summary-template.md` — end-of-session review
- `examples/example-coaching-turn.md` — example interaction

## Core loop

1. Ingest role/company/candidate material.
2. Ask one realistic question.
3. Let the candidate answer without hints.
4. Probe if the answer lacks depth.
5. Score reasoning, product accuracy, and communication.
6. Correct inaccuracies before they become memorized.
7. Turn validated gaps into compact flashcards.
8. Track recurring concept, vocabulary, recall, product, and communication gaps.
9. Increase difficulty from concepts → tradeoffs → failure modes → executive explanation.

The package is deliberately vendor-neutral. Supply company documentation and a role
description to specialize it for Vercel, Cloudflare, AWS, Fireblocks, or another target.
