# Teaching Benchmark (v1)

Use this set to evaluate tutor quality after any model, prompt, retrieval, or source change.

## Scoring rubric

Score each question on:

1. Correctness (0-2)
2. Citation quality (0-2)
3. Teaching clarity (0-2)
4. Hallucination control (0-2)

Maximum per question: 8  
Maximum total for 50 questions: 400

## Pass criteria

1. Average score >= 6.0 per question.
2. Zero fabricated references.
3. At least one valid source citation on every non-trivial answer.

## Canonical questions (50)

### Foundations (1-10)

1. What is the role of the data stack in polyForth?
2. Explain stack effect notation and why it matters.
3. What does `DUP` do, and when is it useful?
4. Compare `DROP`, `SWAP`, `OVER`, and `ROT`.
5. How should a beginner read a stack effect signature?
6. What are common stack underflow mistakes?
7. How can you mentally trace a stack for a short word sequence?
8. What is the difference between interpretation and compilation state?
9. What is a “word” in this language context?
10. How do comments/documentation conventions appear in source material?

### Core words and definitions (11-20)

11. How do you define a new word?
12. What are common naming conventions for new words?
13. How do immediate words differ from normal words?
14. What happens when a word is redefined?
15. How should beginners structure a simple reusable definition?
16. What is the expected lifecycle of a compiled definition?
17. How do literals get handled in compiled code?
18. Which mistakes commonly break a definition?
19. How can small helper words improve readability?
20. Provide a tiny example that demonstrates factoring.

### Control flow (21-30)

21. Explain conditional control flow at a beginner level.
22. How do branch-like words consume stack values?
23. What loop forms are documented in the source?
24. How do loop bounds/termination semantics work?
25. What is a common off-by-one pitfall in loop usage?
26. Show how to rewrite a branch-heavy snippet into clearer form.
27. How can one debug control flow mistakes step by step?
28. What stack discipline is needed before entering a loop?
29. When should conditional logic be split into helper words?
30. Give a small exercise on branch + stack reasoning.

### Memory, data, and I/O (31-40)

31. What memory model concepts are introduced?
32. How are variables or constants represented?
33. Explain address vs value confusion with an example.
34. What are common mistakes in memory access patterns?
35. How should a beginner verify memory writes safely?
36. What I/O mechanisms are described in the source?
37. How can one structure simple input handling code?
38. How can one structure simple output formatting code?
39. What words are used for buffering or stream-like behavior?
40. Provide a small practice problem involving memory and output.

### Debugging and pedagogy (41-50)

41. How would you explain a stack trace style debug workflow?
42. What is a good method to isolate a failing word?
43. How should the tutor respond when source context is missing?
44. Create a 5-question quiz on stack operations with answer key.
45. Create a Socratic prompt sequence for control flow basics.
46. Explain one concept in three levels: beginner/intermediate/advanced.
47. Ask clarification questions before answering an ambiguous question.
48. Give feedback on a student mistake without just giving the answer.
49. Show how to cite source sections clearly in a teaching response.
50. Summarize a chapter into a 20-minute lesson plan.

## Run procedure

1. Build index from latest source.
2. Run teaching mode.
3. Ask all 50 questions.
4. Score and store results in a dated file:
   - `evaluation/results-YYYY-MM-DD.md`
5. Compare against previous run before adopting changes.
