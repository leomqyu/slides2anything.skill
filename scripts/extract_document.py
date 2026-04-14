#!/usr/bin/env python3
"""Extract structured text from PPT/PDF inputs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import zlib
from pathlib import Path
from typing import Iterable

from extract_ppt import extract_pptx, maybe_convert_ppt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text from .ppt, .pptx, or .pdf files, or from a directory containing them."
    )
    parser.add_argument(
        "input_file",
        help="Path to a .ppt/.pptx/.pdf file, or a directory containing those files",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format",
    )
    parser.add_argument("--output", help="Write result to file instead of stdout")
    return parser.parse_args()


def sanitize_items(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = re.sub(r"\s+", " ", item).strip()
        if len(cleaned) < 2 or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def decode_shifted_pdf_text(raw: str) -> str:
    visible = raw.replace("\x00", "")
    visible = "".join(
        ch for ch in visible if unicodedata.category(ch) != "Cc" or ch in "\t\n\r "
    )
    if not visible:
        return visible

    shifted = "".join(
        chr(ord(ch) + 29) if 38 <= ord(ch) <= 93 else ch for ch in visible
    )
    caesar = "".join(
        chr((ord(ch) - ord("A") - 3) % 26 + ord("A")) if "A" <= ch <= "Z"
        else chr((ord(ch) - ord("a") - 3) % 26 + ord("a")) if "a" <= ch <= "z"
        else ch
        for ch in visible
    )

    def englishish_score(text: str) -> int:
        lowered = text.lower()
        letters = sum(ch.isalpha() for ch in text)
        vowels = sum(ch in "aeiou" for ch in lowered)
        bad = sum(not (ch.isalnum() or ch.isspace() or ch in ".,:;!?-_/()[]{}'\"") for ch in text)
        common = sum(lowered.count(token) for token in (
            "the", "ing", "ion", "tion", "and", "for", "with", "that", "this",
            "precision", "arith", "comput", "error", "intro", "table", "number",
        ))
        return letters + vowels * 2 + common * 6 - bad * 8

    candidates = [visible, shifted, caesar]
    return max(candidates, key=englishish_score)


def normalize_pdf_items(items: Iterable[str]) -> list[str]:
    decoded = [decode_shifted_pdf_text(item).strip() for item in items]
    merged: list[str] = []
    for item in decoded:
        if not item:
            continue
        if (
            merged
            and re.fullmatch(r"[A-Za-z]{1,8}", merged[-1])
            and re.fullmatch(r"[a-z]{1,20}", item)
        ):
            merged[-1] += item
            continue
        merged.append(item)
    return sanitize_items(merged)


def decode_pdf_literal(raw: str) -> str:
    output: list[str] = []
    i = 0
    while i < len(raw):
        ch = raw[i]
        if ch != "\\":
            output.append(ch)
            i += 1
            continue
        i += 1
        if i >= len(raw):
            break
        esc = raw[i]
        mapping = {
            "n": "\n",
            "r": "\r",
            "t": "\t",
            "b": "\b",
            "f": "\f",
            "\\": "\\",
            "(": "(",
            ")": ")",
        }
        if esc in mapping:
            output.append(mapping[esc])
            i += 1
            continue
        if esc.isdigit():
            digits = esc
            i += 1
            for _ in range(2):
                if i < len(raw) and raw[i].isdigit():
                    digits += raw[i]
                    i += 1
                else:
                    break
            output.append(chr(int(digits, 8)))
            continue
        output.append(esc)
        i += 1
    return "".join(output)


def pdf_streams(data: bytes) -> list[bytes]:
    pattern = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.DOTALL)
    streams: list[bytes] = []
    for match in pattern.finditer(data):
        stream = match.group(1)
        try:
            streams.append(zlib.decompress(stream))
        except zlib.error:
            streams.append(stream)
    return streams


def parse_pdf_page_text(data: bytes) -> list[str]:
    texts: list[str] = []
    for stream in pdf_streams(data):
        text = stream.decode("latin-1", errors="ignore")
        texts.extend(decode_pdf_literal(m.group(1)) for m in re.finditer(r"\((.*?)\)\s*Tj", text, re.DOTALL))
        texts.extend(bytes.fromhex(m.group(1)).decode("latin-1", errors="ignore") for m in re.finditer(r"<([0-9A-Fa-f]+)>\s*Tj", text))
        for arr in re.finditer(r"\[(.*?)\]\s*TJ", text, re.DOTALL):
            texts.extend(decode_pdf_literal(m.group(1)) for m in re.finditer(r"\((.*?)\)", arr.group(1), re.DOTALL))
            texts.extend(bytes.fromhex(m.group(1)).decode("latin-1", errors="ignore") for m in re.finditer(r"<([0-9A-Fa-f]+)>", arr.group(1)))
    return normalize_pdf_items(texts)


def extract_pdf_with_pdftotext(input_path: Path) -> list[dict[str, object]] | None:
    binary = shutil.which("pdftotext")
    if not binary:
        return None
    completed = subprocess.run(
        [binary, str(input_path), "-"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return None
    raw_pages = re.split(r"\f+", completed.stdout)
    pages: list[dict[str, object]] = []
    for index, page in enumerate(raw_pages, start=1):
        items = normalize_pdf_items(page.splitlines())
        if not items:
            continue
        pages.append(
            {
                "unit_number": index,
                "unit_label": "Page",
                "title": items[0],
                "text": items,
                "notes": [],
            }
        )
    return pages


def extract_pdf_fallback(input_path: Path) -> list[dict[str, object]]:
    data = input_path.read_bytes()
    page_blocks = re.split(rb"/Type\s*/Page\b", data)
    pages: list[dict[str, object]] = []
    page_number = 0
    for block in page_blocks[1:]:
        page_number += 1
        items = parse_pdf_page_text(block)
        if not items:
            continue
        pages.append(
            {
                "unit_number": page_number,
                "unit_label": "Page",
                "title": items[0],
                "text": items,
                "notes": [],
            }
        )
    if not pages:
        raise SystemExit(
            "No extractable PDF text was found. If this is a scanned PDF, OCR is required."
        )
    return pages


def extract_pdf(input_path: Path) -> list[dict[str, object]]:
    return extract_pdf_with_pdftotext(input_path) or extract_pdf_fallback(input_path)


def extract_presentation(input_path: Path) -> list[dict[str, object]]:
    normalized_input = maybe_convert_ppt(input_path)
    slides = extract_pptx(normalized_input)
    return [
        {
            "unit_number": slide["slide_number"],
            "unit_label": "Slide",
            "title": slide["title"],
            "text": slide["text"],
            "notes": slide["notes"],
        }
        for slide in slides
    ]


def list_supported_files(input_path: Path) -> list[Path]:
    supported = {".ppt", ".pptx", ".pdf"}
    if input_path.is_file():
        return [input_path]
    files: list[Path] = []
    for path in sorted(input_path.rglob("*")):
        if path.is_file() and path.suffix.lower() in supported:
            files.append(path)
    return files


def extract_single_file(input_path: Path) -> list[dict[str, object]]:
    suffix = input_path.suffix.lower()
    if suffix in {".ppt", ".pptx"}:
        return extract_presentation(input_path)
    if suffix == ".pdf":
        return extract_pdf(input_path)
    raise SystemExit("Input must be a .ppt, .pptx, or .pdf file.")


def extract_document(input_path: Path) -> list[dict[str, object]]:
    if input_path.is_dir():
        files = list_supported_files(input_path)
        if not files:
            raise SystemExit("No supported files found in the directory.")
        units: list[dict[str, object]] = []
        for file_path in files:
            for unit in extract_single_file(file_path):
                unit["source"] = str(file_path)
                units.append(unit)
        return units
    units = extract_single_file(input_path)
    for unit in units:
        unit["source"] = str(input_path)
    return units


def format_markdown(units: Iterable[dict[str, object]], source: Path) -> str:
    header = f"Source directory: `{source}`" if source.is_dir() else f"Source: `{source}`"
    lines = ["# Extracted Content", "", header, ""]
    for unit in units:
        label = unit["unit_label"]
        number = unit["unit_number"]
        title = unit["title"]
        text = unit["text"]
        notes = unit["notes"]
        source_file = unit.get("source")
        if source.is_dir() and source_file:
            lines.append(f"Source file: `{source_file}`")
            lines.append("")
        lines.append(f"## {label} {number}: {title}")
        lines.append("")
        lines.append("Text:")
        if text:
            for item in text:
                lines.append(f"- {item}")
        else:
            lines.append("- (no text found)")
        if notes:
            lines.append("")
            lines.append("Notes:")
            for item in notes:
                lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_file).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    units = extract_document(input_path)
    if args.format == "json":
        rendered = json.dumps(
            {
                "source": str(input_path),
                "source_type": "directory" if input_path.is_dir() else "file",
                "units": units,
            },
            ensure_ascii=False,
            indent=2,
        )
    else:
        rendered = format_markdown(units, input_path)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
