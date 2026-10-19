---
name: codebase-xray
description: Explain how a technical concept actually works in a specific repository by tracing routes, imports, tool calls, data contracts, streaming, and failure boundaries. Use when the user asks which files implement behavior, wants to understand code, or needs a verified current-vs-proposed architecture map.
---

# Codebase X-Ray

## Goal

Help the learner **own** the implementation: exact file, who calls whom, what is returned, and where an architectural claim is or is not supported.

## Procedure

1. Inspect only the relevant repo/file scope first. If the repo or files are unavailable, say so and ask for the smallest useful set of files. Never invent filenames or content.
2. Find the **entry point** and trace the causal path: UI or event → transport/route → server logic → tools/services → authoritative data → output.
3. Explain type/interface contracts at boundaries: inputs, schemas, response fields, runtime validation vs TypeScript compile time.
4. For async systems, trace separately: model context, UI event/data stream, persistence/side effects, and error/retry path. Do not assume they are the same path.
5. Report exact relevant file paths and small code excerpts. Identify which observations are verified from code and which are hypotheses.
6. If asked about a change, map: requirement → affected boundary → minimal files → preserved files → test/verification. No edits without request/authorization.
7. Ask for ONE teach-back if this is a learning session; prioritize a real causal question such as "How does the client know which route to POST to?"

## High-risk distinctions

- Model prose != authoritative UI facts.
- System prompt != access-control policy.
- API key/service authentication != merchant/tenant authorization != private network reachability.
- A tool wrapper can call a shared API client; deterministic code can call that same client without prompting the model.
- A Next.js Route Handler does not instantiate a durable workflow by itself.
- Server Components are not a replacement for authentication/authorization.

## Report format (adapt to request)

- **One-sentence mechanism**
- **Request/data flow** (plain text diagram if useful)
- **File-by-file evidence**
- **What could fail / be misinterpreted**
- **One interview-ready explanation**

Never report an unobserved feature as implemented. If the user asked only to inspect and plan, deliver the inspection and plan; do not stop at "files read".
