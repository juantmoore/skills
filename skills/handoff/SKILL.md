---
name: handoff
description: Use when a long or context-heavy session needs to pass work to a fresh agent, or when asked to /handoff, write or check a handoff doc, or prep context for a spec. Writes or audits HANDOFF.md.
---

# Handoff

Goal: capture what a fresh agent can't get from reading the files: the why, the dead ends, and my preferences. Link to files instead of copying them. A fresh agent can read the disk, but it can't read your memory.

## Modes
- Write: no HANDOFF.md exists. Create one at the project root using the checklist.
- Audit: HANDOFF.md exists. Check it against the checklist, list the gaps, then make targeted edits. Don't rewrite sections that are already fine.

## Checklist (every section must be present, or marked "none" or "unknown")
1. Status: one paragraph covering what this is, what's done, and what's next.
2. Map: folders and key files, each with a one-line purpose. Mark entry points. Include related repos or folders outside the project root, and say whether each is under git (committed, uncommitted, or not a repo).
3. Run and regenerate: exact commands, env or venv, models used, rough timings, and any setup (for example, LM Studio models that need to be loaded). Flag every command that overwrites deliverables, and say what to back up first.
4. Decisions: each decision with why it was made and what was rejected.
5. Failures and gotchas: what didn't work and why, so nobody retries it.
6. My preferences and constraints: local-first, tools, tone, anything I corrected you on.
7. Skills and tools: each skill or script, where it lives, what it does, and how to invoke it.
8. Open items: known bugs, unfinished work, and questions for me.
9. Next task brief: the goal, which existing pieces to reuse, and open design questions. This is NOT a full spec. The next agent writes the spec.
10. Verify: how to confirm things work (commands, expected outputs).

## Rules
- Verify every path and command you list actually exists (ls or a dry run). Fix or flag anything stale.
- Verify claims about results, not just that commands run. If the doc says a command "reproduces" or "produces" something, run it into a scratch copy and diff. Never dry-run a command that overwrites deliverables in place.
- Rescue anything the work depends on that lives only in temp or scratch dirs (one-off scripts, intermediate data). Copy it into the project and map it, or flag it as at risk.
- Record runtime state left behind (loaded models, running servers, background jobs) and how to stop it.
- Mark anything from a compacted summary, or anything you're unsure about, as "(unverified)".
- Keep it scannable. If a section runs past ~15 lines, link to a file instead.
- Never paste secrets or API keys. Name where they're stored.

## Finish with
1. A short report: what was missing or stale, and what you changed.
2. A paste-ready kickoff prompt for the fresh agent that tells it to:
   a. read HANDOFF.md and the linked files,
   b. read the docs for any framework it's targeting,
   c. use plan mode to write SPEC.md (goals, capabilities, what to reuse, inputs and outputs, acceptance criteria, open questions),
   d. stop for my review before building anything.

## Habit tip
In long sessions, keep a running DECISIONS.md and append a line whenever something gets settled. That makes handoffs cheap.
