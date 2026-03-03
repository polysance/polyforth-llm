# polyforth-llm Roadmap

## Mission

Build a durable polyForth teaching assistant that remains useful for years, with stable operations, measurable quality, and incremental capability growth.

## Principles

1. Reliability before novelty.
2. Source-grounded answers with citations.
3. Track quality with repeatable benchmarks.
4. Prefer reversible changes and versioned artifacts.

## Year 1 milestones

### Quarter 1: Stable baseline

1. Lock host setup (Debian + cooling + thermals).
2. Freeze Python/tooling versions.
3. Run teaching mode daily on source document.
4. Establish benchmark cadence (weekly or per change).

Deliverables:

- Stable `.env` profiles.
- First benchmark report.
- First issue log from real tutoring sessions.

### Quarter 2: Teaching quality

1. Expand chapter-aware lesson templates.
2. Add learner levels (`beginner`, `intermediate`).
3. Add better “missing context” behavior.
4. Tune retrieval parameters with benchmark feedback.

Deliverables:

- Improved tutor prompts.
- Prompt changelog.
- Better benchmark scores on explanation quality.

### Quarter 3: Learning loop

1. Capture failed explanations and misconceptions.
2. Add spaced repetition prompts for weak topics.
3. Create canonical lesson tracks by topic.
4. Add session logs and progress summaries.

Deliverables:

- `teaching_sessions/` records.
- Reusable lesson plans.
- Regression test set from past failures.

### Quarter 4: Hardening

1. Define release process for source updates.
2. Add backup and restore for index/config/profiles.
3. Build monthly quality report.
4. Prepare for optional hardware upgrade path.

Deliverables:

- Release checklist.
- Backup/restore docs.
- Monthly benchmark dashboard (markdown is fine).

## 3-year direction

1. Strong tutor with consistent pedagogy and citation discipline.
2. Multi-document knowledge versioning (spec + examples + errata).
3. Structured curriculum engine with level progression.
4. Optional local-first inference after hardware upgrades.

## Change policy

Before merging significant changes:

1. Run benchmark set.
2. Compare against previous baseline.
3. Document any quality regression and mitigation.

## Risks and mitigations

1. Source drift:
   - Mitigation: versioned source docs and index rebuild log.
2. Prompt regressions:
   - Mitigation: benchmark gate before adoption.
3. Hardware instability:
   - Mitigation: thermal checks before long workloads.
4. Overfitting to one document:
   - Mitigation: add curated examples and exercises over time.
