<div align="center">

# slides2anything.skill

English | [中文](README.ZH.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blueviolet.svg)](https://openai.com)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

> *"Turn fragmented slides into usable final study files for review, note-taking, and exams."*

<br>

Still staring at a deck full of bullets, formulas, and half-finished lecture notes?<br>
Still rebuilding PDF handouts into something that reads like real course material?<br>
Still wasting time writing transitions, definitions, examples, summaries, and review questions by hand?<br>

**slides2anything** is a skill for turning `.ppt`, `.pptx`, and `.pdf` sources into high-value study outputs such as realistic cheatsheets, notes, and textbook chapters.  
It does not stop at raw extraction. It helps the agent ask for missing context, read the source, and then use its own LLM writing ability to produce directly usable final files for exam cramming, note-taking, revision, and teaching.

<br>

Accepts slide decks and PDF documents<br>
Outputs **cheatsheets / notes / textbook chapters / exercises with answers** in **Markdown / Word DOCX / LaTeX**<br>
Lets the agent ask for file paths, output format, and writing mode before it starts

[Requirements](#requirements) · [How It Works](#how-it-works) · [Example Prompts](#example-prompts) · [Notes](#notes)

</div>

---

## Why It Feels Different

| Typical workflow | slides2anything |
|------|------|
| Extracts text and leaves you with raw fragments | Extracts first, then helps the agent turn fragments into a usable final study file |
| Assumes the first prompt already contains every parameter | Prompts the agent to ask for missing paths, format, structure, and mode |
| Treats PPT and PDF as plain text sources | Treats them as teaching material with implied structure and pedagogy |
| Produces flat notes or rigid templates | Uses the model to write realistic cheatsheets, revision notes, teacher notes, summaries, formulas, and full teaching text |
| Exports a file | Produces a final output intended to be directly usable for study, revision, and exam prep |

In short: this project is designed for **teaching-oriented and exam-oriented rewriting**, especially for **college students doing exam cramming or building clean notes fast**, not just text extraction.

## Features

- Supports single files or batch folder input (PPT/PPTX/PDF)
- Cheatsheet mode focuses on hard formulas and likely exam points
- Teacher notes, textbook chapters, and revision notes are all supported
- Exercises-with-answers output mode
- LaTeX output also compiles to PDF
- Formula-preserving output for DOCX and LaTeX

## Requirements

This skill works best when the environment includes:

- Python 3, for source extraction
- LibreOffice, if you need to convert legacy `.ppt` files into `.pptx`
- Pandoc, if you want the final result exported as `.docx`
- TeX Live (or a LaTeX engine like `xelatex`) if you want LaTeX to compile into PDF
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
3. The extractor reads the PPT/PDF source (or all files inside a folder).
4. The agent uses the extracted material as grounding.
5. The agent writes the requested cheatsheet, notes, or textbook output with its own LLM capabilities.
6. The result is saved as Markdown, LaTeX (plus compiled PDF), or exported to DOCX.

When the output is a cheatsheet, the agent should ask for the target page count and treat it as a hard constraint. Keep whitespace minimal and layout tight.

## Example Prompts

Users do not need to write commands. Natural language is enough.

Examples:

- Please use `slides2anything` to turn my PPT into a cheatsheet for exam review.
- Use `slides2anything` to make a final exam cheatsheet from my lecture slides.
- Use `slides2anything` to make a 2-page cheatsheet from my lecture slides, and ask me the target page count first if I forget it.
- Use `slides2anything` to turn my PDF into clean revision notes for a college midterm.
- Please use `slides2anything` on my PDF handout and ask me for the missing file path and output format first.
- I want to turn a lecture deck into teacher notes. Use `slides2anything` and guide me through the missing options.
- Use `slides2anything` to generate exercises with answers from my lecture deck.
- Use `slides2anything` to create a LaTeX textbook draft from my PDF, but ask me what structure I want before you start.

The agent should normally ask for:

- the PPT or PDF path
- the desired output path
- the output format: Markdown, DOCX, or LaTeX
- the target mode: cheatsheet, teacher notes, textbook, exercises with answers, notes, or student handout
- for cheatsheets, the approximate target page count
- whether to include learning objectives, glossary, summary, and exercises

For example, in a cheatsheet workflow, a good follow-up question is:

- `If this should be a cheatsheet, about how many pages should it target?`

## Notes

- For `.ppt` inputs, the extractor will try to convert the file with `libreoffice` or `soffice`.
- For `.pdf` inputs, the extractor prefers system PDF text tools when available and falls back to an internal parser otherwise.
- For LaTeX output, the agent should compile a PDF using `xelatex` when available (especially for Chinese).
- For folder input, the extractor will read all supported files inside the directory and synthesize a combined output.
