#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path


INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def with_base_path(path: str) -> str:
    if "://" in path or path.startswith(("#", "/", "mailto:", "tel:")):
        return path
    return f"../{path}"


def convert_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = LINK_RE.sub(
        lambda match: f'<a href="{with_base_path(match.group(2))}">{match.group(1)}</a>',
        escaped,
    )
    escaped = BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)
    return escaped


def flush_paragraph(lines: list[str], out: list[str]) -> None:
    if not lines:
        return
    content = " ".join(line.strip() for line in lines)
    out.append(f"<p>{convert_inline(content)}</p>")
    lines.clear()


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        if not line.strip():
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        rows.append(parts)

    if len(rows) < 2:
        return ""

    header = rows[0]
    body = rows[2:]
    header_html = "".join(f"<th>{convert_inline(cell)}</th>" for cell in header)
    body_html = []
    for row in body:
        body_html.append(
            "<tr>" + "".join(f"<td>{convert_inline(cell)}</td>" for cell in row) + "</tr>"
        )
    return (
        "<table>"
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(body_html)}</tbody>"
        "</table>"
    )


def markdown_to_html(md_text: str, title: str) -> str:
    out: list[str] = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []
    list_open = False
    table_lines: list[str] = []

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            out.append("</ol>")
            list_open = False

    def close_table() -> None:
        nonlocal table_lines
        if table_lines:
            out.append(render_table(table_lines))
            table_lines = []

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip("\n")

        if line.strip().startswith("```"):
            close_table()
            flush_paragraph(paragraph, out)
            close_list()
            if in_code:
                out.append(
                    "<pre><code>"
                    + html.escape("\n".join(code_lines))
                    + "</code></pre>"
                )
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if line.strip().startswith("|") and line.strip().endswith("|"):
            flush_paragraph(paragraph, out)
            close_list()
            table_lines.append(line)
            continue
        else:
            close_table()

        if not line.strip():
            flush_paragraph(paragraph, out)
            close_list()
            continue

        if line.startswith("## "):
            flush_paragraph(paragraph, out)
            close_list()
            out.append(f"<h2>{convert_inline(line[3:])}</h2>")
            continue

        if line.startswith("![") and "](" in line and line.endswith(")"):
            flush_paragraph(paragraph, out)
            close_list()
            alt = line[line.find("[") + 1 : line.find("]")]
            src = line[line.find("(") + 1 : -1]
            out.append(
                "<figure>"
                f'<img src="{html.escape(with_base_path(src))}" alt="{html.escape(alt)}" />'
                f"<figcaption>{html.escape(alt)}</figcaption>"
                "</figure>"
            )
            continue

        if line.startswith("> "):
            flush_paragraph(paragraph, out)
            close_list()
            out.append(f"<blockquote>{convert_inline(line[2:])}</blockquote>")
            continue

        if re.match(r"^\d+\.\s+", line):
            flush_paragraph(paragraph, out)
            close_table()
            if not list_open:
                out.append("<ol>")
                list_open = True
            item_text = re.sub(r"^\d+\.\s+", "", line)
            out.append(f"<li>{convert_inline(item_text)}</li>")
            continue

        paragraph.append(line)

    close_table()
    flush_paragraph(paragraph, out)
    close_list()

    body = "\n".join(out)
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(title)}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #1f2937;
      line-height: 1.55;
      margin: 36px auto;
      max-width: 900px;
      padding: 0 24px 48px;
    }}
    h2 {{
      margin-top: 28px;
      margin-bottom: 12px;
      font-size: 24px;
      border-bottom: 2px solid #e5e7eb;
      padding-bottom: 6px;
    }}
    p, li, blockquote, td, th {{
      font-size: 15px;
    }}
    ol {{
      padding-left: 24px;
    }}
    code {{
      background: #f3f4f6;
      border-radius: 4px;
      padding: 1px 4px;
      font-size: 0.95em;
    }}
    pre {{
      background: #111827;
      color: #f9fafb;
      border-radius: 10px;
      padding: 14px 16px;
      overflow-x: auto;
      white-space: pre-wrap;
    }}
    pre code {{
      background: transparent;
      padding: 0;
      color: inherit;
    }}
    blockquote {{
      margin: 16px 0;
      padding: 10px 14px;
      border-left: 4px solid #93c5fd;
      background: #eff6ff;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
    }}
    th, td {{
      border: 1px solid #d1d5db;
      padding: 8px 10px;
      vertical-align: top;
      text-align: left;
    }}
    th {{
      background: #f3f4f6;
    }}
    figure {{
      margin: 18px 0 22px;
    }}
    img {{
      max-width: 100%;
      height: auto;
      border: 1px solid #d1d5db;
      border-radius: 8px;
      display: block;
    }}
    figcaption {{
      color: #6b7280;
      font-size: 13px;
      margin-top: 6px;
    }}
    a {{
      color: #1d4ed8;
      text-decoration: none;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    practice_root = Path(__file__).resolve().parent.parent
    md_path = practice_root / "README.md"
    html_dir = practice_root / "generated"
    html_path = html_dir / "testit_practice_5_report.html"
    md_text = md_path.read_text(encoding="utf-8")
    html_text = markdown_to_html(md_text, "Практическая работа 5. TestIT")
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html_text, encoding="utf-8")
    print(html_path)


if __name__ == "__main__":
    main()
