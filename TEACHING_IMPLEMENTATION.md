# Teaching Mode Implementation Plan

This implementation track is focused on polyForth instruction quality, not heavy autonomous coding.

## Objective

Deliver a tutor experience that helps learners progress from basics to intermediate fluency.

## Current implementation

Implemented entrypoint:

- `python scripts/teaching_chat.py`

Implemented modes:

1. `explain`
2. `socratic`
3. `quiz`

Implemented capabilities:

1. Context retrieval from indexed source document.
2. Citation-first answers.
3. Quiz generation with answer key.

## Immediate teaching rollout

1. Build index from source doc:
   - `python scripts/build_index.py`
2. Start teaching mode:
   - `python scripts/teaching_chat.py`
3. Run first lesson sequence:
   - Stack model
   - Core words
   - Control flow
   - Memory concepts
4. Run end-of-lesson quiz:
   - `/quiz <topic> 5`

## Suggested curriculum blocks

1. Foundations
   - Stack effects
   - Data stack operators
   - Interpreter/compiler state
2. Core construction
   - Defining words
   - Control flow
   - Loops
3. Practical usage
   - Memory and variables
   - I/O patterns
   - Debugging idioms

## Acceptance checklist

1. Every lesson response includes at least one citation.
2. Socratic mode asks clarifying questions before full answer.
3. Quiz mode returns both questions and answer key.
4. Tutor says "missing context" when source does not support answer.

## Next improvements

1. Add lesson templates per chapter.
2. Add learner level profiles (`beginner`, `intermediate`).
3. Add spaced repetition queue from wrong quiz answers.
4. Add progress logs in `teaching_sessions/`.
