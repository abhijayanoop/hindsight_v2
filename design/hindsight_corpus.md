# Hindsight Seeded Incident Corpus

**What this is:** 24 synthetic-but-plausible LLM production incident write-ups. These are the raw text you feed to `cognee.add()`. Cognee's LLM extracts entities and relations from them; the ontology grounds those into the graph.

**How it's engineered (read before editing):** These are NOT random. The interconnections are deliberate, because traversal needs something to traverse. Specifically:

- **Shared artifact cluster:** INC-002, INC-009, INC-014, INC-021 all touch the *Ticket Summarizer Prompt*. This lets the graph link them even when their text differs.
- **Shared cause pattern (for memify):** INC-002, INC-009, INC-014, INC-021 are all *regressions caused by a prompt change*. Four instances of one pattern is what lets `memify` derive the rule "gate prompt changes behind an eval." Without repetition, there's no pattern to derive.
- **The recurrence pair (the demo's heart):** INC-002 (early) and INC-021 (late) are *causally identical* — a prompt edit silently degraded summary quality — but described in completely different words. Vector search will miss the link (different wording); graph search will catch it (same artifact + same cause type). This pair IS demo beats 1-2.
- **The belief-revision target (the closer):** INC-014 is written with a *plausible but wrong* root cause (it blames a model change when the real cause was the prompt edit). This gives the `forget` demo something to retract, after which dependent reasoning should update.
- **Cost cluster:** INC-004, INC-011, INC-019 share the max_tokens-bump cause pattern, a second derivable rule.

When demoing, your "new incoming incident" is a freshly-written paraphrase of INC-002's situation (see the demo script) — NOT one of these 24. These 24 are the memory; the new one is the test.

Each record follows the five-part shape: what went wrong / how noticed / cause / artifacts touched / how fixed. Dates establish temporal order for `temporal_cognify`.

---

## INC-001 — 2026-01-08 — RAG breakage
The onboarding assistant began answering setup questions with outdated steps. Detected via a spike in user reports ("these instructions don't match the new UI"). Root cause: the doc search index was rebuilt with a new embedding model, but the old chunks weren't re-embedded, so retrieval mixed two embedding spaces and returned stale docs. Affected the Doc Search Index and the Onboarding Assistant Prompt. Fixed by fully re-embedding the corpus and adding an index-version check (a guardrail) before serving.

## INC-002 — 2026-01-15 — Regression
The ticket summarizer started producing vaguer summaries that dropped key account details. Caught by the Summary Quality Eval Suite: faithfulness score fell from 0.91 to 0.79. Root cause: an engineer edited the Ticket Summarizer Prompt to handle a new ticket category, and the rewrite weakened the instruction to always preserve account IDs. Affected the Ticket Summarizer Prompt and the Summary Quality Eval Suite. Fixed by reverting the prompt edit (rollback) and adding an eval gate so prompt changes can't ship if faithfulness drops.

## INC-003 — 2026-01-19 — Latency
P95 latency on the support deployment doubled from 1.2s to 2.6s. Detected via the latency dashboard alert. Root cause: a config change raised max_tokens from 512 to 2048 for a feature that rarely needed long outputs, so generation ran longer on every call. Affected the Support Feature Deployment. Fixed by lowering max_tokens back to 768 (config fix).

## INC-004 — 2026-01-23 — Cost spike
Daily token spend on the support feature jumped 3.4x overnight. Detected via a cost alert. Root cause: the same max_tokens bump from the latency incident also inflated billed output tokens across all traffic. Affected the Support Feature Deployment. Fixed by reverting the max_tokens config and adding a budget alert (guardrail).

## INC-005 — 2026-01-29 — Outage
The summarizer feature returned errors for 40 minutes. Detected via error-rate alert. Root cause: the model provider deprecated an older model snapshot we had pinned, and requests started 404ing. Affected the Support Feature Deployment and its pinned Model. Fixed by switching to the current model snapshot (rollback to a supported version) and adding a deprecation-watch guardrail.

## INC-006 — 2026-02-03 — RAG breakage
Search answers in the onboarding assistant became irrelevant for queries about billing. Detected via user reports. Root cause: a data change — a batch of billing docs was deleted during a cleanup, so retrieval had nothing relevant to pull. Affected the Doc Search Index. Fixed by restoring the docs and adding a corpus-size guardrail that alerts on large deletions.

## INC-007 — 2026-02-07 — Regression
The onboarding assistant began refusing reasonable questions, replying "I can't help with that." Caught by an eval drop in task-completion rate. Root cause: a prompt change added an over-broad safety clause to the Onboarding Assistant Prompt. Affected the Onboarding Assistant Prompt. Fixed by narrowing the clause (prompt fix).

## INC-008 — 2026-02-12 — Cost spike
Token spend rose 60% with no traffic increase. Detected via cost alert. Root cause: a config change enabled an aggressive retry policy (3 retries on any non-200), and a flaky upstream caused frequent retries, each a full billed call. Affected the Support Feature Deployment. Fixed by capping retries at 1 with backoff (config fix).

## INC-009 — 2026-02-18 — Regression
Summaries from the ticket summarizer started omitting the resolution status of tickets. Caught by the Summary Quality Eval Suite (a targeted check on status fields). Root cause: a prompt change to the Ticket Summarizer Prompt reordered the output template and the status field fell outside the truncation window. Affected the Ticket Summarizer Prompt and the Summary Quality Eval Suite. Fixed by restoring field order and adding an eval gate on status presence (guardrail).

## INC-010 — 2026-02-24 — Latency
Onboarding assistant responses slowed during peak hours. Detected via latency alert. Root cause: a model change to a larger, slower model for "better quality" without load testing. Affected the Onboarding Assistant Prompt's deployment and the Model. Fixed by reverting to the smaller model for this low-complexity task (rollback).

## INC-011 — 2026-03-02 — Cost spike
Monthly spend forecast blew past budget mid-month. Detected via cost metric trending. Root cause: a config change raised max_tokens on the onboarding feature to allow longer answers, inflating cost on every call. Affected the Onboarding Assistant deployment. Fixed by setting a per-feature max_tokens cap (config fix + guardrail).

## INC-012 — 2026-03-08 — RAG breakage
The onboarding assistant cited a competitor's product name in answers. Detected via user report. Root cause: a data change ingested an unfiltered scraped doc set into the Doc Search Index. Affected the Doc Search Index. Fixed by re-filtering ingestion and adding a source-allowlist guardrail.

## INC-013 — 2026-03-14 — Outage
Both features went down for 25 minutes. Detected via error-rate alert. Root cause: a dependency change — the provider SDK was auto-upgraded and changed a default parameter name, breaking calls. Affected the Support Feature Deployment and Onboarding deployment. Fixed by pinning the SDK version (rollback) and adding a dependency-pin guardrail.

## INC-014 — 2026-03-20 — Regression
The ticket summarizer's summaries became noticeably blander and lost specific dollar amounts. Caught by the Summary Quality Eval Suite. The on-call engineer attributed it to a model change that had happened around the same time and switched the model back, which did not help. The real cause, found later, was a prompt change to the Ticket Summarizer Prompt that softened the instruction to quote exact figures. Affected the Ticket Summarizer Prompt and the Summary Quality Eval Suite. Eventually fixed by reverting the prompt edit (rollback) and tightening the eval gate. [NOTE: this record intentionally carries a misattributed initial cause — the ModelChange — for the belief-revision demo.]

## INC-015 — 2026-03-26 — Latency
Summarizer p95 latency spiked intermittently. Detected via latency alert. Root cause: a dependency change — the provider introduced rate-based throttling and our client retried without backoff, compounding delays. Affected the Support Feature Deployment. Fixed by adding exponential backoff (config fix).

## INC-016 — 2026-04-01 — RAG breakage
Doc search returned near-duplicate chunks, crowding out diverse results. Detected via user report of "repetitive answers." Root cause: a data change re-ingested the corpus without dedup, so the Doc Search Index filled with duplicates. Affected the Doc Search Index. Fixed by re-running ingestion with dedup and adding a dedup guardrail.

## INC-017 — 2026-04-07 — Cost spike
Spend rose sharply on the summarizer. Detected via cost alert. Root cause: a prompt change added several verbose few-shot examples to the Ticket Summarizer Prompt, inflating input tokens on every call. Affected the Ticket Summarizer Prompt. Fixed by trimming the examples (prompt fix) and adding an input-token budget check (guardrail).

## INC-018 — 2026-04-13 — Regression
Onboarding answers became inconsistent in tone, sometimes overly casual. Caught by an eval drop in tone-consistency. Root cause: a config change raised temperature from 0.2 to 0.8 during an experiment that wasn't reverted. Affected the Onboarding Assistant deployment. Fixed by restoring temperature (config fix).

## INC-019 — 2026-04-19 — Cost spike
Token spend on support climbed steadily over a week. Detected via cost trending. Root cause: a config change enabled streaming with a high max_tokens default, and outputs ran to the cap. Affected the Support Feature Deployment. Fixed by lowering max_tokens and adding a budget guardrail.

## INC-020 — 2026-04-25 — Outage
Onboarding assistant failed for all users for 15 minutes. Detected via error-rate alert. Root cause: a dependency change — an expired API key on a rotated credential wasn't updated in one environment. Affected the Onboarding deployment. Fixed by rotating the key correctly and adding a key-expiry guardrail.

## INC-021 — 2026-05-02 — Regression
Account managers complained that ticket recaps had gotten "fluffy" and were leaving out the specific customer identifiers they rely on. The weekly quality check confirmed a measurable drop in how faithfully summaries reflected source tickets. Investigation traced it to a recent revision of the summarizer's instructions that was meant to make summaries more readable but, as a side effect, relaxed the requirement to always include identifying account fields. The summarizer prompt and the quality eval were both involved. Resolved by undoing the instruction revision and reinstating the pre-merge eval check that blocks quality drops. [NOTE: this is the recurrence twin of INC-002 — same cause, same artifact, deliberately different vocabulary so vector search misses the link and graph search catches it.]

## INC-022 — 2026-05-08 — Latency
Support summarizer latency degraded after a deploy. Detected via latency alert. Root cause: a model change to a reasoning-heavy model that "thinks" longer per call, unnecessary for summarization. Affected the Support Feature Deployment and the Model. Fixed by reverting to the faster model (rollback).

## INC-023 — 2026-05-14 — RAG breakage
Onboarding answers grew confidently wrong on edge-case setup steps. Detected via user reports. Root cause: a data change shrank the chunk size during a tuning experiment, splitting procedures mid-step so retrieval returned partial instructions. Affected the Doc Search Index. Fixed by restoring chunk size (config fix) and adding a retrieval-quality eval (guardrail).

## INC-024 — 2026-05-20 — Regression
The onboarding assistant began hallucinating menu paths that don't exist. Caught by an eval drop in factual-accuracy. Root cause: a prompt change removed the instruction to only reference documented features. Affected the Onboarding Assistant Prompt. Fixed by restoring the grounding instruction (prompt fix) and adding a factuality eval gate (guardrail).
