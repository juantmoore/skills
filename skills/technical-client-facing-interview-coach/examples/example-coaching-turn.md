# Example Coaching Turn

## Interviewer
A global e-commerce customer needs fast page loads, but product descriptions can be
an hour old while inventory must be nearly real time. How would you architect it?

## Candidate
[Candidate answers.]

## Coach

### 🟢 Strengths
- Correctly separated stable and dynamic content.
- Connected performance to global caching.

### 🟡 Gaps / Missed Details
- Did not define how inventory avoids stale shared cache.
- Did not explain where dynamic compute should run relative to the inventory system.

### 🔴 Technical Corrections
- Incremental revalidation is a freshness/caching mechanism; it is not synonymous
  with streaming.
- "Run at the edge" is not automatically faster when the source of truth is in one region.

### 🔵 Reframing
"At a high level, I'd separate the page by freshness requirement. Stable catalog
content can be globally cached and revalidated, while inventory stays dynamic and is
fetched through compute located near the inventory source of truth. I'd stream or
defer the dynamic portion so it doesn't block the reusable shell. Then I'd validate
cache hit rate, TTFB, inventory accuracy, and conversion."

### Score
- Architecture/reasoning: 8/10
- Product/company accuracy: 7/10
- Communication: 8/10

### Probe
What changes if the inventory API starts timing out during a flash sale?

Do not generate the flashcard until the candidate understands the correction.
