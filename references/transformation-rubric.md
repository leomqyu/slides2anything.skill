# Transformation Rubric

Use this rubric after extracting slide content and before drafting the final textbook text.

## Structural Mapping

- Treat title or agenda slides as candidate chapter or section boundaries.
- Merge consecutive slides that cover one idea into a single subsection.
- If a slide contains only keywords, borrow context from adjacent slides before rewriting.

## Textbook Expansion Heuristics

- Bullet list to prose: explain the relation between bullets instead of listing them unchanged.
- Diagram placeholder: describe the purpose of the diagram if the textual content implies one, but do not hallucinate visual details that are absent from text or notes.
- Formula slide: keep the formula verbatim when possible, then explain variables, intuition, and usage conditions.
- Procedure slide: convert into ordered steps with prerequisites and expected outcome.
- Comparison slide: rewrite as contrastive prose or a two-column comparison only if the user wants tabular output.
- Sparse slide to textbook prose: if a slide contains only terms or short phrases, expand it into teachable prose by drawing on adjacent slides and the chapter context.
- Heading to content: never leave a heading unsupported. Every heading in the output should be followed by meaningful explanation.
- Source to standalone text: rewrite material so that the reader does not need to see the original slides. Avoid phrases that point back to the PPT or PDF as a prerequisite.

## Cheatsheet Heuristics

- If the requested mode is `速查表` / `cheatsheet`, compress aggressively.
- Prefer formulas, definitions, ranges, mappings, conversion steps, code patterns, and high-yield comparisons.
- Explicitly emphasize difficult formulas, tricky conversion steps, and likely exam points from both student and teacher perspectives.
- Minimize connective prose; maximize retrieval value for exam review.
- Use tables or tightly structured bullets when they improve density.
- Include symbolic notation whenever the chapter materially depends on it.
- If a target page count is given, treat it as a hard constraint. If over, compress; if under, add dense summary tables or comparison grids to reach the target.

## Exercises With Answers

- If the requested mode is `习题与答案` / `exercises with answers`, generate questions that map directly to the extracted content.
- Provide clear, correct answers immediately after each question.
- Mix question types when appropriate: definitions, conversions, comparisons, application problems, and explanation prompts.

## Minimum Substance Standard

- A textbook section should usually contain at least one real explanatory paragraph, not just a list of labels.
- A summary should synthesize ideas, not repeat the table of contents.
- Key terms should come from the source chapter and should not be left as an empty heading.
- Exercises should test actual chapter knowledge, not generic filler questions.
- Teacher notes should contain actionable classroom guidance, not just renamed chapter headings.

## Recommended Default Chapter Shape

1. Chapter title
2. Learning objectives
3. Introductory overview
4. Sectioned main content
5. Key concepts or glossary
6. Summary
7. Practice questions

## Hallucination Guardrails

- If the slide deck lacks enough context, say which point is ambiguous.
- Avoid adding references, standards, or historical facts unless they are present in the source or supplied by the user.
- Do not turn a mnemonic bullet into a precise claim unless the deck states the claim clearly.

## Style Targets

- Prefer complete declarative sentences.
- Use explicit transitions such as "因此", "进一步来看", "换句话说", "由此可见" only where they clarify logic.
- Keep terminology stable: one concept, one Chinese translation unless the source itself uses aliases.
- When the deck is technical, preserve English terms at first mention in parentheses when useful.
- Favor high-information paragraphs over shallow summary phrases.
- Write so that the reader can learn from the text even without seeing the original slides.
- When formulas matter, do not paraphrase them away; write them explicitly.
