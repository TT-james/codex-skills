#!/usr/bin/env python3
"""Convert a Markdown AI case into a Word-compatible .doc HTML file."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def inline(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def parse_table(lines: list[str], start: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        raw = lines[i].strip().strip("|")
        cells = [inline(cell) for cell in raw.split("|")]
        if not all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in raw.split("|")):
            rows.append(cells)
        i += 1

    if not rows:
        return "", i

    parts = ["<table>"]
    for idx, cells in enumerate(rows):
        tag = "th" if idx == 0 else "td"
        parts.append("<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in cells) + "</tr>")
    parts.append("</table>")
    return "\n".join(parts), i


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    parts: list[str] = []
    list_stack: list[str] = []
    i = 0

    def close_lists() -> None:
        while list_stack:
            parts.append(f"</{list_stack.pop()}>")

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped:
            close_lists()
            i += 1
            continue

        if stripped.startswith("|"):
            close_lists()
            table_html, i = parse_table(lines, i)
            parts.append(table_html)
            continue

        match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if match:
            close_lists()
            level = min(len(match.group(1)), 4)
            parts.append(f"<h{level}>{inline(match.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith(">"):
            close_lists()
            parts.append(f"<blockquote>{inline(stripped.lstrip('>').strip())}</blockquote>")
            i += 1
            continue

        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        if ordered or unordered:
            tag = "ol" if ordered else "ul"
            if not list_stack or list_stack[-1] != tag:
                close_lists()
                parts.append(f"<{tag}>")
                list_stack.append(tag)
            parts.append(f"<li>{inline((ordered or unordered).group(1))}</li>")
            i += 1
            continue

        close_lists()
        parts.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_lists()
    return "\n".join(parts)


def render_doc(markdown: str, title: str) -> str:
    body = markdown_to_html(markdown)
    title_html = html.escape(title)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="ProgId" content="Word.Document">
<meta name="Generator" content="Codex ai-promotion-case-doc">
<title>{title_html}</title>
<style>
@page Section1 {{ size: 21cm 29.7cm; margin: 2.2cm 2.4cm 2.2cm 2.4cm; }}
div.Section1 {{ page: Section1; }}
body {{ font-family: "Microsoft YaHei", SimSun, Arial, sans-serif; font-size: 11pt; line-height: 1.65; color: #1f2933; background: #ffffff; }}
h1 {{ font-family: "Microsoft YaHei", SimHei, sans-serif; font-size: 22pt; text-align: center; margin: 0 0 16pt; color: #17365d; font-weight: bold; }}
h2 {{ font-family: "Microsoft YaHei", SimHei, sans-serif; font-size: 16pt; margin: 18pt 0 10pt; color: #17365d; font-weight: bold; border-bottom: 1.5pt solid #4f81bd; padding-bottom: 4pt; }}
h3 {{ font-family: "Microsoft YaHei", SimHei, sans-serif; font-size: 13pt; margin: 14pt 0 8pt; color: #1f4e79; font-weight: bold; }}
h4 {{ font-family: "Microsoft YaHei", SimHei, sans-serif; font-size: 11.5pt; margin: 10pt 0 6pt; color: #1f4e79; font-weight: bold; }}
p {{ margin: 5pt 0; }}
ul, ol {{ margin: 4pt 0 8pt 22pt; padding: 0; }}
li {{ margin: 3pt 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 10.5pt; }}
th {{ background: #d9eaf7; color: #17365d; font-weight: bold; }}
th, td {{ border: 1pt solid #9eb6ce; padding: 6pt 8pt; vertical-align: top; }}
blockquote {{ border-left: 3pt solid #4f81bd; margin: 8pt 0; padding: 4pt 10pt; background: #f3f7fb; }}
code {{ font-family: Consolas, "Courier New", monospace; background: #f3f4f6; padding: 1pt 3pt; }}
</style>
</head>
<body>
<div class="Section1">
{body}
</div>
</body>
</html>
"""


def infer_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            return match.group(1).strip()
    return fallback


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to a Word-compatible .doc HTML file.")
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--output", required=True, help="Output .doc file")
    parser.add_argument("--title", help="Document title")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    markdown = input_path.read_text(encoding="utf-8")
    title = args.title or infer_title(markdown, input_path.stem)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_doc(markdown, title), encoding="utf-8", newline="\r\n")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
