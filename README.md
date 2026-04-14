<div align="center">

# slides2anything

English | [中文](README_ZH.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blueviolet.svg)](https://openai.com)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

> *"Turn fragmented slides into cheatsheets, notes, and study material you can actually use."*

<br>

Still staring at a deck full of bullets, formulas, and half-finished lecture notes?<br>
Still rebuilding PDF handouts into something that reads like real course material?<br>
Still wasting time writing transitions, definitions, examples, summaries, and review questions by hand?<br>

**slides2anything** is a skill for turning `.ppt`, `.pptx`, and `.pdf` sources into high-value study outputs.  
It does not stop at raw extraction. It helps the agent ask for missing context, read the source, and then use its own LLM writing ability to produce exam-oriented cheatsheets, teacher notes, and textbook-quality content.

<br>

Accepts slide decks and PDF documents<br>
Outputs **cheatsheets / notes / textbook drafts** in **Markdown / Word DOCX / LaTeX**<br>
Lets the agent ask for file paths, output format, and writing mode before it starts

[Requirements](#requirements) · [How It Works](#how-it-works) · [Example Prompts](#example-prompts) · [Notes](#notes)

</div>

---

## Why It Feels Different

| Typical workflow | slides2anything |
|------|------|
| Extracts text and leaves you with raw fragments | Extracts first, then helps the agent turn fragments into teachable chapters |
| Assumes the first prompt already contains every parameter | Prompts the agent to ask for missing paths, format, structure, and mode |
| Treats PPT and PDF as plain text sources | Treats them as teaching material with implied structure and pedagogy |
| Produces flat notes or rigid templates | Uses the model to write cheatsheets, teacher notes, summaries, formulas, and full teaching text |
| Exports a file | Produces a draft that is actually usable for teaching, editing, and publishing |

In short: this project is designed for **teaching-oriented and exam-oriented rewriting**, not just text extraction.

## Requirements

This skill works best when the environment includes:

- Python 3, for source extraction
- LibreOffice, if you need to convert legacy `.ppt` files into `.pptx`
- Pandoc, if you want the final result exported as `.docx`
- Optionally `pdftotext`, which can improve PDF extraction quality when available

If you only work with `.pptx`, you may not need LibreOffice.
If you only want Markdown or LaTeX, you do not need Pandoc.

## Project Layout

- `SKILL.md`: the main skill instructions
- `scripts/extract_ppt.py`: PowerPoint extraction
- `scripts/extract_document.py`: unified extractor for PPT and PDF inputs
- `references/transformation-rubric.md`: rewriting heuristics for dense, high-value study output
- `agents/openai.yaml`: skill metadata

## How It Works

The intended workflow is:

1. The user asks for a study output in natural language.
2. The agent asks follow-up questions if key information is missing.
3. The extractor reads the PPT or PDF source.
4. The agent uses the extracted material as grounding.
5. The agent writes the requested cheatsheet, notes, or textbook draft with its own LLM capabilities.
6. The result is saved as Markdown, LaTeX, or exported to DOCX.

This is an important design choice: the actual output should be written by the agent, not by a rigid template script.

## Example Prompts

Users do not need to write commands. Natural language is enough.

Examples:

- Please use `slides2anything` to turn my PPT into a cheatsheet for exam review.
- Please use `slides2anything` on my PDF handout and ask me for the missing file path and output format first.
- I want to turn a lecture deck into teacher notes. Use `slides2anything` and guide me through the missing options.
- Use `slides2anything` to create a LaTeX textbook draft from my PDF, but ask me what structure I want before you start.

The agent should normally ask for:

- the PPT or PDF path
- the desired output path
- the output format: Markdown, DOCX, or LaTeX
- the target mode: cheatsheet, teacher notes, textbook, or student handout
- whether to include learning objectives, glossary, summary, and exercises

## Notes

- For `.ppt` inputs, the extractor will try to convert the file with `libreoffice` or `soffice`.
- For `.pdf` inputs, the extractor prefers system PDF text tools when available and falls back to an internal parser otherwise.
- For `.docx` output, `pandoc` is used only as an export step after the agent has already written the content.
- If the source contains formulas, symbols, or conversion processes, the agent should write them directly into the final output rather than referring back to the slides.
- This project is designed to generate a strong first draft, not to fabricate missing subject matter that is absent from the source.
