# Example lesson shape (illustrative, not a current-product specification)

**Question:** What is a durable workflow, and why would an agent need one?

**Business:** A merchant reconciliation investigation may call multiple slow APIs. If request execution fails halfway through, repeating expensive work wastes time and money.

**Mental model:** A workflow is a tracked, resumable sequence of work. It isn't simply a larger timeout or a chat-history buffer.

**Mechanism:** Start run → execute step A → record successful step output → execute step B → if B fails, apply retry policy → resume/retry from an appropriate checkpoint instead of blindly redoing all work. Actual replay and side-effect rules depend on implementation: verify them in the chosen framework.

**Architecture decision:** Move work that must survive process termination into durable execution. Keep simple, short-lived synchronous lookups synchronous if durable coordination is not justified.

**Enterprise trade-off:** Better recovery, but more infrastructure/operational model to reason about; side effects need idempotency.

**Teach-back:** What is the difference between "the model remembers earlier chat" and "a workflow resumes a previously completed API step"?
