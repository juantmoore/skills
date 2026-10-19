# SA Interview Story Coach

A reusable prompt skill for preparing Solutions Architects, Solutions Engineers, Sales Engineers, TAMs, Forward Deployed Engineers, and other customer-facing technical candidates.

## What it does

- Mines raw career recollections into structured interview stories.
- Creates a durable JSON story library.
- Maps stories to interview competencies.
- Builds fast retrieval cues and STAAARL index cards.
- Runs realistic one-question-at-a-time mock interviews.
- Separately coaches Sales/GTM, Product/EPD, and technical architecture answers.
- Reviews practice transcripts and identifies better story choices.
- Flags missing evidence and story portfolio gaps instead of fabricating details.

## Best inputs

1. Job description and recruiter/interview brief.
2. Resume.
3. Performance reviews or brag documents.
4. Existing `interview-stories.json`.
5. Raw voice-note-style story recollections.
6. Public artifacts such as blog posts, repos, demos, or docs when available.

## Suggested starting request

> Review my role materials, resume, and story library. Build a competency map for each interview stage. Then identify the 5 stories I should make retrieval-ready first. Do not rewrite the stories yet. Show me coverage gaps and ask me for the highest-value missing story.

## Story-building request

> I am going to give you a raw story from memory. Extract the facts, identify the strongest decision arc, flag anything that needs verification, convert it into the canonical story JSON, and create a concise STAAARL card and retrieval map. Do not invent metrics or outcomes.

## Mock interview request

> Run a Product mock interview. Ask one question at a time. After each answer, give Strengths, Gaps, Reframing, Story Fit, Retrieval Cue, and one likely follow-up. Stay on the same question if I did not demonstrate the judgment being tested.

