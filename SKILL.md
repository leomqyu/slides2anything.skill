---
name: slides2anything
description: Transform a PowerPoint deck or PDF document into useful study outputs. Use this skill when the user provides a .ppt, .pptx, or .pdf file and wants a cheatsheet（中文可译为“速查表”）, notes, teacher notes, textbook-style prose, formulas, summaries, exercises, or other structured learning material derived from the source content.
---

# Slides To Anything

Use this skill when the input is a slide deck or PDF handout and the target output is a high-value learning artifact rather than bullets or fragmented pages. By default, prefer a cheatsheet / 速查表 unless the user explicitly asks for textbook prose, teacher notes, or another mode.

## Conversation Policy

Do not assume the user already provided every parameter in one prompt. If any of the following are missing, ask for them explicitly before generating the output:

- the PPT file path
- or the PDF file path
- the desired output path
- the target mode
- whether the user wants Markdown, DOCX, or LaTeX
- whether they want a cheatsheet, notes, teacher notes, textbook prose, or student handout style
- any required chapter structure such as learning objectives, glossary, summary, or exercises

When asking follow-up questions, keep them short and concrete. Prefer asking for the minimum information needed to proceed.
Match the user's language:

- If the user asks in Chinese, ask in Chinese and prefer Chinese mode labels such as `速查表`、`笔记`、`教师讲义`、`教材正文`。
- If the user asks in English, ask in English and prefer English labels such as `cheatsheet`, `notes`, `teacher notes`, `textbook chapter`.
- In English interactions, do not switch back to Chinese-only labels when asking about options.

Recommended default questions in Chinese:

1. 你的 PPT 或 PDF 文件路径是什么？
2. 你希望输出到哪个路径？
3. 你想要哪种模式：速查表、笔记、教师讲义、教材正文，还是学生讲义？
4. 你希望输出为 Markdown、DOCX，还是 LaTeX？
5. 你是否需要学习目标、关键术语、小结和练习题？

Recommended default questions in English:

1. What is the path to your PPT or PDF file?
2. Where should I save the output?
3. Which mode do you want: cheatsheet, notes, teacher notes, textbook chapter, or student handout?
4. Which output format do you want: Markdown, DOCX, or LaTeX?
5. Do you want learning objectives, key terms, a summary, and practice questions?

When asking about the mode, mention the options in this order: `速查表` / `cheatsheet` first, `笔记` / `notes` second, `教师讲义` / `teacher notes` third, `教材正文` / `textbook chapter` fourth, and then any other modes if relevant.

If the user does not specify a mode after being asked, default to `速查表` in Chinese interactions and `cheatsheet` in English interactions.
If the user does not specify an output format after being asked, default to `Markdown`.

## Inputs

- `.pptx`: supported directly
- `.ppt`: supported if `libreoffice` or `soffice` is installed locally so it can be converted to `.pptx`
- `.pdf`: supported directly; text-based PDFs work best

## Quick Workflow

1. Check whether the file path, output path, mode, and output format are known. If not, ask the user first.
2. Run the bundled extractor to get slide-by-slide or page-by-page source text.
3. Read the extracted content and infer the structure: chapter, section, concept flow, examples, and missing transitions.
4. Use your own LLM writing ability to rewrite the material into the requested study format. Do not rely on a rigid template generator.
5. Rewrite into the requested mode:
   - for `速查表` / `cheatsheet`, prefer formulas, definitions, conversion rules, ranges, contrasts, and compact reminders
   - for `笔记` / `notes`, produce clean revision-oriented notes with slightly more connective explanation
   - for `教材正文` / `textbook chapter`, expand bullet points into full explanatory prose
   - preserve formulas, symbols, names, and ordered procedures
   - clearly mark uncertain or underspecified content instead of fabricating details
6. Save the result in the requested format:
   - `Markdown`: write the output directly as `.md`
   - `LaTeX`: write the output directly as `.tex`
   - `DOCX`: first prepare the content as Markdown, then convert it with `pandoc` if available
7. Return the result in the format the user asked for. If unspecified after clarification, default to:
   - title
   - concise high-yield structure for the chosen mode
   - key terms or formulas when relevant
   - short recap if it fits the mode

## Extraction

Run the bundled extractor first when you need a slide-by-slide or page-by-page inspection pass.

```bash
python3 scripts/extract_document.py /absolute/path/to/input.pptx
```

Useful variants:

```bash
python3 scripts/extract_document.py /absolute/path/to/input.pdf --format json
python3 scripts/extract_document.py /absolute/path/to/input.ppt --output /tmp/deck.md
```

The extractor outputs slide-by-slide or page-by-page text. After extraction, you should write the final study output yourself using the extracted content and the user-requested mode.

## Generation Policy

- The actual output must be written by the agent, not by a hard-coded templating script.
- Use the extracted source as grounding, then synthesize fluent study-oriented or teaching-oriented text with the model.
- If the user asks for a richer or more polished output, spend effort on explanation quality, transitions, examples, and conceptual clarity instead of falling back to canned wording.
- If the source is sparse, say what is underspecified instead of pretending the source contained more than it did.
- If the user asks for DOCX, write the content first, then export it with `pandoc` only as a packaging step.
- The final output must read as a standalone learning resource. Do not assume the reader has already seen the slides, PPT, or PDF.
- Do not write sentences like “课件中给出了……”, “PPT 中展示了……”, “从上面的幻灯片可以看出……”, or similar references that make the source deck a prerequisite for understanding.
- If the source contains an example, formula, or conversion process, restate it directly in the output as part of the teaching material.
- Do not output a hollow scaffold made of section headings with little or no prose underneath.
- Do not stop at labels such as `正文`, `关键术语`, `本章小结`, or `练习题`; each requested section must contain substantive content.
- Treat every major section as a writing task, not a placeholder. If a section is included, fill it with real explanatory material.

## Content Density Requirements

- `教材正文` must contain substantial prose under each major section, not just 1 to 2 generic sentences.
- `笔记` should feel like clean, high-quality revision notes rather than fragmented bullets.
- For each core subsection inferred from the source, usually write at least 1 coherent explanatory paragraph. For important subsections, write 2 or more paragraphs when the source supports it.
- `学习目标` should be concrete and teachable, not empty slogans.
- `关键术语` should list actual concepts from the source, preferably with short explanations when useful.
- `本章小结` should synthesize the chapter's main ideas in paragraph form, not merely restate the headings.
- `练习题` should be tied to the chapter content and test understanding, comparison, conversion, explanation, or application.
- `教师讲义` should include real teaching guidance such as sequencing, emphasis, likely misconceptions, and usable classroom prompts.
- `速查表` should be compact, exam-oriented, and information-dense. Favor formulas, conversion rules, ranges, definitions, comparison tables, and minimal but high-yield reminders.
- If the user asks for `速查表`, aggressively compress wording while preserving the highest-value exam content.
- The default `速查表` / `cheatsheet` mode should be especially suitable for college students doing exam cramming or organizing fast notes.
- If the source chapter is long, the output should also be correspondingly substantial. Do not compress a full chapter into a few thin paragraphs.

## Anti-Laziness Rules

- Never produce an outline-only answer when the user asked for textbook content.
- Never produce a low-information cheatsheet that is only headings plus a few vague bullets.
- Never output section titles with blank bodies or near-empty bodies.
- Never pad with generic phrases like “本节主要介绍相关内容” unless followed by concrete explanation.
- If a section feels thin, expand it by explaining definitions, relationships, examples, contrasts, engineering implications, or common mistakes.
- Before finalizing, check whether a teacher or student could learn from the prose alone. If not, expand it.
- Never rely on the phrase “课件里已经给出” or any equivalent shortcut instead of actually presenting the needed content.

## Writing Rules

- Convert fragments into the level of completeness appropriate for the selected mode.
- Keep terminology consistent across the whole output.
- Preserve the original pedagogical order unless the deck is obviously disorganized.
- When slides are sparse, infer only the minimum connective explanation needed for readability.
- Do not invent citations, data values, experimental results, or claims absent from the deck.
- If a slide appears to be an outline, use it to structure downstream sections.
- If speaker notes exist, treat them as high-value author intent.
- Prefer explanation over mere listing. A bullet in the source should usually become explanation, not another bullet in the output.
- When introducing a concept, explain what it is, why it matters, and how it relates to nearby concepts.
- When comparing representations or encodings, make the difference explicit instead of leaving it implied.
- Present examples directly as teaching examples. Do not frame them as references to the source file.
- If the source contains formulas or symbolic relations, preserve them and use them actively in the output.
- For `DOCX` output, try to include equations in a form that `pandoc` can convert cleanly into Word equations when possible.
- For `LaTeX` output, be more formula-rich and explicit with notation than in prose-only formats.

## Output Modes

Choose the closest mode to the user request.

- `速查表`: concise, high-density, exam-oriented summary sheet; in English contexts this should be called `cheatsheet`
- `笔记`: revision-oriented notes; in English contexts this should be called `notes`
- `教材正文`: formal, sectioned textbook prose
- `教师讲义`: more explanatory, includes teaching transitions
- `学生讲义`: simpler wording, stronger summaries
- `习题扩展`: derive review questions and short exercises from the source deck

If the user does not specify a mode, produce `速查表` / `cheatsheet` depending on the interaction language.

## When To Read More

- For rewriting standards and expansion heuristics, read [references/transformation-rubric.md](references/transformation-rubric.md).
