#!/usr/bin/env python3
"""Extract slide text and notes from a .pptx deck.

Supports legacy .ppt input by converting it to .pptx with libreoffice/soffice
when available.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract slide text and notes from a PowerPoint file."
    )
    parser.add_argument("input_file", help="Path to .ppt or .pptx file")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--output",
        help="Write result to file instead of stdout",
    )
    return parser.parse_args()


def numeric_suffix(path: str, prefix: str) -> int:
    match = re.search(rf"{re.escape(prefix)}(\d+)\.xml$", path)
    return int(match.group(1)) if match else 10**9


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[1] if "}" in tag else tag


def extract_text_from_xml(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    pieces: list[str] = []
    for node in root.iter():
        if local_name(node.tag) != "p":
            continue
        text = "".join(
            child.text or ""
            for child in node.iter()
            if local_name(child.tag) == "t"
        ).strip()
        if text:
            pieces.append(text)
    return pieces


def maybe_convert_ppt(input_path: Path) -> Path:
    if input_path.suffix.lower() != ".ppt":
        return input_path

    office_binary = shutil.which("libreoffice") or shutil.which("soffice")
    if not office_binary:
        raise SystemExit(
            "Legacy .ppt detected, but libreoffice/soffice is not installed. "
            "Convert the file to .pptx first or install LibreOffice."
        )

    temp_dir = Path(tempfile.mkdtemp(prefix="slides2anything-"))
    command = [
        office_binary,
        "--headless",
        "--convert-to",
        "pptx",
        "--outdir",
        str(temp_dir),
        str(input_path),
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise SystemExit(
            "LibreOffice conversion failed:\n"
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )

    converted = temp_dir / f"{input_path.stem}.pptx"
    if not converted.exists():
        raise SystemExit("Conversion reported success but no .pptx output was produced.")
    return converted


def read_zip_text_map(zf: zipfile.ZipFile, prefix: str) -> dict[int, list[str]]:
    result: dict[int, list[str]] = {}
    names = sorted(
        (name for name in zf.namelist() if name.startswith(prefix) and name.endswith(".xml")),
        key=lambda name: numeric_suffix(name, Path(prefix).name),
    )
    for name in names:
        number = numeric_suffix(name, Path(prefix).name)
        if number == 10**9:
            continue
        result[number] = extract_text_from_xml(zf.read(name))
    return result


def extract_pptx(input_path: Path) -> list[dict[str, object]]:
    with zipfile.ZipFile(input_path) as zf:
        slides = read_zip_text_map(zf, "ppt/slides/slide")
        notes = read_zip_text_map(zf, "ppt/notesSlides/notesSlide")

    deck: list[dict[str, object]] = []
    for slide_number in sorted(slides):
        slide_text = slides.get(slide_number, [])
        note_text = notes.get(slide_number, [])
        title = slide_text[0] if slide_text else f"Slide {slide_number}"
        deck.append(
            {
                "slide_number": slide_number,
                "title": title,
                "text": slide_text,
                "notes": note_text,
            }
        )
    return deck


def format_markdown(deck: Iterable[dict[str, object]], source: Path) -> str:
    lines = [f"# Extracted Slides", "", f"Source: `{source}`", ""]
    for slide in deck:
        slide_number = slide["slide_number"]
        title = slide["title"]
        text = slide["text"]
        notes = slide["notes"]

        lines.append(f"## Slide {slide_number}: {title}")
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

    if input_path.suffix.lower() not in {".ppt", ".pptx"}:
        raise SystemExit("Input must be a .ppt or .pptx file.")

    normalized_input = maybe_convert_ppt(input_path)
    deck = extract_pptx(normalized_input)

    if args.format == "json":
        rendered = json.dumps(
            {
                "source": str(input_path),
                "normalized_input": str(normalized_input),
                "slides": deck,
            },
            ensure_ascii=False,
            indent=2,
        )
    else:
        rendered = format_markdown(deck, input_path)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
