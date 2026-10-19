# Example Vercel SA Curriculum

This is a study roadmap, not a source of current product capability claims. Validate product details in official docs before teaching.

## Foundation

- Next.js: routing, server/client boundaries, data fetching, caching, rendering, streaming.
- Vercel Functions & Fluid Compute: request lifecycle, concurrency, compute vs waiting, regions, limits.
- Edge/CDN/caching: cache scope, freshness, personalization, invalidation, trade-offs.

## AI and durable applications

- AI SDK: `useChat`, tools, ToolLoopAgent, streaming, runtime schemas, evals.
- AI Gateway: model access boundary, governance/cost/observability claims with docs verification.
- Workflows: durable steps, retries, idempotency, continuation, compensating actions.
- Eve: distinguish framework abstractions from underlying Workflows/AI SDK/Sandbox capabilities; verify current APIs.
- Sandbox: isolation, input/output handling, security and when it is actually necessary.

## Enterprise/production

- Hybrid and multi-cloud: where truth lives, network reachability, auth, authorization, private paths.
- Operational readiness: observability, quotas, backpressure, reliability, cost, rollout and rollback.
- Agent correctness: authoritative-data boundaries, tool selection, deterministic invariants, regression evals.

## Example case studies to reuse

1. **Mr. Reconcile:** browser → Next.js `/api/chat` → agent → narrow tools → AWS financial data; generated explanation vs deterministic UI facts.
2. **Private AWS API:** replacing public HTTPS with a private network path without redesigning the web UX.
3. **Mandatory financial lookup:** application code enforces critical checks; agent retains optional exploration/explanation.
4. **10,000 merchants:** investigate end-to-end metrics before asserting a bottleneck.

For each topic, aim for: 30-second explanation, runtime diagram, one code reference when available, a trade-off, a production failure case, and an answer for a nontechnical buyer.
