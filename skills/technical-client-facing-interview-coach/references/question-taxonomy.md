# Question Taxonomy

Use these patterns to create realistic interview scenarios. Customize them to the
target company's architecture and products.

## 1. Rendering / caching / freshness
- Global commerce site with catalog, price, and inventory changing at different rates.
- News/media site with mostly static pages plus breaking updates.
- SaaS dashboard with public marketing pages and authenticated data.

Probe:
- What can be stale?
- What is user-specific?
- What is the source of truth?
- What invalidates cached content?

## 2. Scalability
- Marketing launch creates a 10x traffic spike.
- Viral event causes unpredictable read traffic.
- AI endpoint suddenly has much higher concurrency.

Probe:
- CDN/cache hit ratio
- dynamic compute
- database connections
- third-party quotas
- rate limiting
- load testing
- operational ownership

## 3. Reliability / dependency failure
- Payment processor unavailable.
- Search provider timing out.
- LLM provider degraded.
- Inventory service returning stale results.

Probe:
- durable state
- idempotency
- timeout
- retries/backoff
- circuit breaker
- fallback
- reconciliation
- customer messaging

## 4. Security / compliance
- PII cannot enter shared caches.
- Data must stay within a geography.
- Private backend cannot be internet-addressable.
- AI workload has retention constraints.

Probe:
- authorization
- caching
- logging
- secrets
- encryption
- network boundaries
- residency / retention
- auditability

## 5. Edge vs regional / data locality
- Global users, centralized database.
- Distributed key/value data plus regional relational DB.
- Authentication/routing at the edge, business logic in-region.

Probe:
"Draw the path: user → compute → data."

## 6. Hybrid / on-prem
- Cloud frontend must access an on-prem ERP.
- Customer is migrating incrementally from legacy infrastructure.
- Backend requires IP allowlisting/private networking.

Probe:
- network path
- auth
- failover
- latency
- caching
- ownership boundary

## 7. Personalization
- Product recommendations after authentication.
- Locale/market customization.
- A/B experiment assignment.
- Personalized account dashboard.

Probe:
- what is common vs per-user?
- what is cacheable?
- where is the profile stored?
- what must render immediately?

## 8. Observability
- Customer reports intermittent latency.
- Conversion dropped after deployment.
- AI responses fail only for one geography.

Probe:
- what signals?
- what baselines?
- trace which dependency?
- what customer KPI?

## 9. AI / agents
- Assistant calls product, inventory, payment, or account tools.
- Agent is moving from prototype to broad rollout.
- Model must never become the source of truth.

Probe:
- tool contracts
- auth
- grounding
- evals
- latency
- failure modes
- guardrails
- observability
- model portability

## 10. Migration / adoption
- Customer already has AWS/GCP/on-prem investments.
- They do not want a rewrite.
- Need an incremental path with measurable wins.

Probe:
- what stays?
- what moves first?
- rollback?
- ownership?
- success metric?

## 11. Developer experience
- Teams deploy slowly.
- Preview/testing environments are inconsistent.
- Frontend and backend ownership is fragmented.

Probe:
- deployment workflow
- environments
- CI/CD
- observability
- platform standards
- governance

## 12. Discovery / stakeholder
- CTO asks for "faster."
- VP Sales wants launch in one month.
- Security says no public network access.
- Product wants personalization everywhere.

Probe:
- turn vague goals into measurable requirements;
- explain tradeoffs to the right stakeholder;
- separate must-have from nice-to-have.
