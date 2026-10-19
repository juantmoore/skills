# Curveball bank — select one at a time

These are scenarios, not answer keys. Adapt to the learner's real stack. Do not assert a product-specific capability without verifying it.

1. **Private AWS:** The customer's API must be unreachable from the public internet. What does the requirement mean, and which network boundary changes? Push if answer is only API keys.
2. **Mandatory evidence:** Model sometimes skips a required financial check. Which steps become application guarantees and where does the code live? Push if answer is only prompts.
3. **Scale:** 10,000 merchants need access. Ask where to *measure first*, before naming bottlenecks. Probe request concurrency, model quota, tool fan-out, AWS capacity, p95 latency, spend and success rate.
4. **Partial failure:** A tenth tool fails after nine expensive successes. What's resumable, retryable, idempotent, and visible to the user? Ask how to test it.
5. **Sensitive data:** An enterprise asks exactly which merchant/financial data is sent to an LLM and how cross-tenant scope is enforced.
6. **No LLM allowed for core money movement:** Preserve deterministic money state and allow AI only for explanations or optional investigation.
7. **Model outage:** Provider becomes unavailable during a high-traffic incident. What is the customer-safe degradation strategy? Avoid claiming automatic failover that hasn't been configured.
8. **Long investigation:** A workflow takes 20 minutes and approval. What changes between synchronous HTTP response and durable asynchronous execution?
9. **AWS migration objection:** CTO wants every backend on Vercel immediately. What needs to be discovered before agreeing to replace the authoritative system?
10. **Canary rollout:** How do you separately roll out infrastructure and merchant adoption; which correctness metrics halt rollout?
11. **Product choice:** Why use a framework/workflow instead of simple Route Handler + agent loop? What requirement justifies the additional moving parts?
12. **Evaluation disagreement:** An answer sounds good but lacks necessary authoritative evidence. How do you catch it with repeatable evals and deterministic checks?

Use a follow-up that tests WHY the initial answer would work, not whether the learner knows a Vercel marketing term.
