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
