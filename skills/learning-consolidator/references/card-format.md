# Index-card format

## Template

**FRONT**

[Interviewer question?]

Probe: [one deeper follow-up, optional]

**BACK**

[70–120 word, first-person, natural spoken explanation; accurately distinguishes today's implementation from a proposed extension. Include cause/effect, not only nouns.]

## Example — deterministic checks

**FRONT**

If an LLM sometimes skips a required financial lookup, how would you guarantee it runs?

Probe: Which code layer would change?

**BACK**

“If a lookup is mandatory, I wouldn't rely on a system prompt or stronger tool description because the model can still skip it. I'd move that check into server-side application orchestration, using the existing backend API client directly, and give the agent the verified result for explanation. I'd keep optional investigation agent-driven where flexibility is useful. In my current POC that guarantee isn't implemented, so this would be a targeted production change. I'd test that the lookup always runs, including failure and retry cases, and keep a separate eval for explanation quality. The principle is: model instructions influence behavior; code enforces guarantees.”

The example is illustrative; use the learner's actual architecture when writing a live card.
