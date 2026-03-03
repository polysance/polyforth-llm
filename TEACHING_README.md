# polyforth-llm Teaching Mode

This document covers the dedicated teaching workflow, separate from general chat usage.

## Purpose

Teaching mode is optimized for:

1. Clear concept explanations.
2. Guided/Socratic tutoring.
3. Quiz generation with answer keys and citations.

## Run teaching mode

```bash
python scripts/teaching_chat.py
```

## Commands

- `/mode explain|socratic|quiz`
- `/lesson <topic>`
- `/quiz <topic> [count]`
- `/help`
- `exit`

## Mode behavior

1. `explain`
   - Direct explanation
   - Small example
   - One short practice task
2. `socratic`
   - Tutor asks focused questions first
   - Then provides guided explanation
3. `quiz`
   - Generates quiz questions + answer key
   - Includes source citations

## Example session

```text
/mode explain
/lesson What is stack effect notation?

/mode socratic
How does DUP differ from OVER?

/quiz Control flow words 6
```

## Quality expectations

1. Answers should cite retrieved sources, e.g. `[section:...]` or `[pX]`.
2. If context is missing, tutor should say what is missing.
3. Explanations should be short, progressive, and focused on fundamentals.
