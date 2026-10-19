# Flashcard Template

| Problem statement | Front | Back |
|---|---|---|
| 1–2 short sentences describing the customer problem. | 3–7 word concept title. | 5–7 compact bullets. |

## Back-card checklist

Try to include:

1. Principle / recommendation
2. Data or request flow
3. Relevant mechanism/product
4. Failure or security consideration
5. Tradeoff
6. Validation / observability
7. Business outcome, when useful

## Example

**Problem statement:**  
A payment provider becomes unavailable during checkout. The application must preserve
the order and recover safely without duplicate charges.

**Front:**  
Graceful Third-Party API Failure

**Back:**
- Persist order/payment state before the external call.
- Use idempotency keys for safe retries.
- Set timeouts and fail quickly when the dependency is unhealthy.
- Retry through durable asynchronous processing with backoff.
- Reconcile final status through provider events/status checks.
- Show the user an honest pending/retry/failed state.
- Monitor failures, retries, queue depth, and unresolved orders.

## Card-writing rules

- Hand-writable, not mini essays.
- One concept per card.
- Prefer mechanisms over marketing language.
- Never encode an unverified vendor claim into a card.
- Replace outdated cards rather than keeping contradictory versions.
