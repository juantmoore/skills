---
source: grok-bot
name: client-workshop-artifacts
description: >-
  Use this after a client workshop deck is finalized and the owner says the deck
  is in their hands. It builds the client's Business Context report and agent
  instruction Docs in their shared Drive folder, mirroring a past client.
---
# Client workshop artifacts (business context + agent instructions)

Source of truth: the Customer Workshop Playbook Google Doc in the business Drive (client workshops folder), stage 6. When this process changes, update both the playbook and this skill, and add a row to the playbook's Lessons learned log.

## When
The order is fixed: finalize the session deck first. Only once the owner says the deck is done or in their hands, build these artifacts so they match what the deck shows. Don't start earlier, since the deck decides which agents get built and which Doc names the slides refer to.

## Inputs
- The client's shared folder in the business Drive, standard layout: `client workshops` › `<Client>` › `<Client> (Shared)`, with `Agent Instructions`, `Business Context`, and `Workshop Recordings & Notes` inside. You need the `Business Context` and `Agent Instructions` folder ids. If a subfolder is missing, create it in that layout; if the client uses an older layout, don't move anything and tell the owner.
- A reference client folder. Read ONLY its `Business Context` and `Agent Instructions` subfolders and ignore recordings and notes.
- The client's planning Doc, especially any copy-paste materials section the deck points to (templates, skill briefs, exact Doc titles).
- Intake facts about the client: who they are, the org, products, tools, accounts and the agents they agreed to build.

## Steps
1. **List both destination folders first** to avoid making duplicates. Never change sharing. The owner shares the folder himself, usually within 24 hours after the session.
2. **Read every file in the reference's two folders.** Note the file names, heading structure, length, voice, and the numbering in build order (`01-<agent>`, `02-<agent>`). Sample-input PDFs show what the agent receives; they aren't context prose.
3. **Read the planning Doc's copy-paste section.** Its template text and Doc titles are the starting content.
4. **Research the client using public professional sources only:** the org site, the parent org (including its current team page, since older sites go stale), press about named products or pilots, and the person's LinkedIn (if it won't load, use search snippets and mark them [verify]). Record every URL. Label intake-only facts "from intake". Flag conflicts between intake and public sources, such as merger dates, rebrands or changed titles.
5. **Write the Business Context report** (`<client-slug>-business-report`, a Google Doc), mirroring the reference sections:
   - Executive Summary with an At a Glance table and Core Conclusions
   - Who the person is
   - What the org builds or sells (a table)
   - Who it serves
   - Mission
   - Operating model: team, stack, tools, AI accounts
   - Chief of Staff operating plan
   - Risks and opportunities
   - Internal positioning
   - Bottom line
   - Research notes listing the [verify] items
   - Sources
6. **Write one Doc per agent** (`01-<agent>`, `02-<agent>`) with these parts:
   - Profile: name, where it lives, connectors and sources, skill, schedule
   - Paste-in Instructions in a code block with CAPS labels: ONE JOB, SOURCES OF TRUTH, WHAT YOU DO, ANTI-JOBS, SCHEDULE, FORMAT, VOICE
   - Setup prompts, sent in order: add context, have it explain its job back, connect and test one source at a time, create the skill (with the brief embedded), run and check, schedule
   - Ongoing prompts
   - Adapt the steps to the client's actual tool. Non-coders get no-code steps only (for example, Claude with connectors and skills).
7. **Create the copy-paste Docs** with the exact titles the deck names: TEMPLATE and Skill brief Docs. Keep the text, fix only internal contradictions and note each fix, and highlight the fill-in [blanks] yellow in the TEMPLATE Docs.
8. **Create the Docs through the business Drive connector** (`create_file` as a Google Doc, markdown for structure, HTML when you need highlights) so they land directly in the target folders.

## Checks
- No em or en dashes. Plain language for a non-coder.
- None of the owner's banned terms for this client, such as employers, series or pricing language, or other sessions. No reference-client or reference-platform names leaking in.
- Every fact is sourced, labeled from intake, or marked [verify]. Number claims say what they count, and self-reported figures are labeled. No personal data beyond public professional info.
- Schedules, sources and rules match what the deck and brief say.
- After creating them, list both folders and spot-read one Doc of each format.

## Report
One line per reference file, each new Doc's title, link and folder, the [verify] list, and anything that couldn't be reconciled. Suggest a Lessons learned row for the playbook if anything surprised you.
