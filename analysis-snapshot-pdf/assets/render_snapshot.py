#!/usr/bin/env python3
"""
Render a structured analysis snapshot to PDF.

Reusable backend for the `analysis-snapshot-pdf` skill. See ../SKILL.md for
the full content schema and invocation patterns.

CLI:
    python3 render_snapshot.py --input content.json --output report.pdf

Python:
    from render_snapshot import render
    render(content_dict, "/path/to/output.pdf")
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
from typing import Any

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------

NAVY = HexColor("#0b3d91")
ACCENT = HexColor("#1a5fb4")
GREY = HexColor("#555555")
LIGHT_GREY = HexColor("#f4f4f4")
RULE = HexColor("#dddddd")


def register_fonts() -> tuple[str, str]:
    """Register a Unicode-capable font family. Returns (regular_name, bold_name)."""
    candidates = [
        (
            "DejaVu",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
        ),
        (
            "Liberation",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
        ),
    ]
    for fam, normal, bold, italic, bolditalic in candidates:
        if not (os.path.exists(normal) and os.path.exists(bold)):
            continue
        try:
            pdfmetrics.registerFont(TTFont(fam, normal))
            pdfmetrics.registerFont(TTFont(f"{fam}-Bold", bold))
            ital_name = fam
            bi_name = f"{fam}-Bold"
            if os.path.exists(italic):
                pdfmetrics.registerFont(TTFont(f"{fam}-Italic", italic))
                ital_name = f"{fam}-Italic"
            if os.path.exists(bolditalic):
                pdfmetrics.registerFont(TTFont(f"{fam}-BoldItalic", bolditalic))
                bi_name = f"{fam}-BoldItalic"
            registerFontFamily(
                fam,
                normal=fam,
                bold=f"{fam}-Bold",
                italic=ital_name,
                boldItalic=bi_name,
            )
            return fam, f"{fam}-Bold"
        except Exception:
            continue
    return "Helvetica", "Helvetica-Bold"


def _make_styles(regular: str, bold: str) -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle(
            "Title", fontName=bold, fontSize=15, leading=18,
            textColor=NAVY, spaceAfter=2,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", fontName=regular, fontSize=9, leading=11,
            textColor=GREY, spaceAfter=10,
        ),
        "meta_label": ParagraphStyle(
            "MetaLabel", fontName=bold, fontSize=8.5, leading=11, textColor=GREY,
        ),
        "meta_value": ParagraphStyle(
            "MetaValue", fontName=regular, fontSize=9.5, leading=12.5, textColor=black,
        ),
        "card_section": ParagraphStyle(
            "CardSection", fontName=bold, fontSize=8.5, leading=11, textColor=white,
        ),
        "card_metric": ParagraphStyle(
            "CardMetric", fontName=regular, fontSize=9, leading=12, textColor=black,
        ),
        "card_value": ParagraphStyle(
            "CardValue", fontName=bold, fontSize=9, leading=12, textColor=black,
        ),
        "section_heading": ParagraphStyle(
            "SectionHeading", fontName=bold, fontSize=12, leading=15,
            textColor=NAVY, spaceBefore=12, spaceAfter=4,
        ),
        "sub_heading": ParagraphStyle(
            "SubHeading", fontName=bold, fontSize=10.5, leading=13,
            textColor=ACCENT, spaceBefore=8, spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "Body", fontName=regular, fontSize=9.5, leading=13,
            textColor=black, spaceAfter=5, alignment=TA_LEFT,
        ),
        "wts_body": ParagraphStyle(
            "WTSBody", fontName=regular, fontSize=9.5, leading=13,
            textColor=black, spaceAfter=8, leftIndent=14,
        ),
        "table_header": ParagraphStyle(
            "TableHeader", fontName=bold, fontSize=9, leading=11.5,
            textColor=white, alignment=TA_LEFT,
        ),
        "table_cell": ParagraphStyle(
            "TableCell", fontName=regular, fontSize=9, leading=12, textColor=black,
        ),
        "table_first_col": ParagraphStyle(
            "TableFirstCol", fontName=bold, fontSize=9, leading=12, textColor=NAVY,
        ),
    }


# ---------------------------------------------------------------------------
# Block renderers
# ---------------------------------------------------------------------------

def _render_card(block: dict, styles: dict, page_width: float) -> list:
    story: list = []
    if block.get("title"):
        story.append(Paragraph(block["title"], styles["section_heading"]))
    rows: list = []
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
    ]
    for group_label, metrics in block.get("groups", []):
        idx = len(rows)
        rows.append([Paragraph(group_label, styles["card_section"]), ""])
        style_cmds.append(("SPAN", (0, idx), (1, idx)))
        style_cmds.append(("BACKGROUND", (0, idx), (1, idx), NAVY))
        style_cmds.append(("TOPPADDING", (0, idx), (1, idx), 5))
        style_cmds.append(("BOTTOMPADDING", (0, idx), (1, idx), 5))
        style_cmds.append(("LINEBELOW", (0, idx), (1, idx), 0, white))
        for metric, value in metrics:
            rows.append([
                Paragraph(metric, styles["card_metric"]),
                Paragraph(value, styles["card_value"]),
            ])
    if rows:
        col1 = page_width * 0.37
        col2 = page_width - col1
        tbl = Table(rows, colWidths=[col1, col2])
        tbl.setStyle(TableStyle(style_cmds))
        story.append(tbl)
    return story


def _render_sections(block: dict, styles: dict) -> list:
    story: list = []
    if block.get("title"):
        story.append(Paragraph(block["title"], styles["section_heading"]))
    label_style = block.get("label_style", "heading")
    for label, body in block.get("items", []):
        bodies = body if isinstance(body, list) else [body]
        if label_style == "inline":
            # First paragraph gets the bold label prefix
            if bodies:
                story.append(Paragraph(f"<b>{label}.</b> {bodies[0]}", styles["body"]))
                for extra in bodies[1:]:
                    story.append(Paragraph(extra, styles["body"]))
            else:
                story.append(Paragraph(f"<b>{label}.</b>", styles["body"]))
        else:
            story.append(Paragraph(label, styles["sub_heading"]))
            for para in bodies:
                story.append(Paragraph(para, styles["body"]))
    return story


def _render_numbered(block: dict, styles: dict) -> list:
    story: list = []
    if block.get("title"):
        story.append(Paragraph(block["title"], styles["section_heading"]))
    for i, (prefix, body) in enumerate(block.get("items", []), 1):
        story.append(
            Paragraph(f"<b>{i}. {prefix}.</b> {body}", styles["wts_body"])
        )
    return story


def _render_table(block: dict, styles: dict, page_width: float) -> list:
    story: list = []
    if block.get("title"):
        story.append(Paragraph(block["title"], styles["section_heading"]))

    headers = block.get("headers", [])
    rows = block.get("rows", [])
    highlight_first_col = block.get("highlight_first_column", True)

    if not rows:
        return story

    n_cols = max(len(headers) if headers else 0, max((len(r) for r in rows), default=0))
    if n_cols == 0:
        return story

    table_data: list = []
    if headers:
        table_data.append([Paragraph(h, styles["table_header"]) for h in headers])
    for row in rows:
        cells = []
        for col_idx, cell in enumerate(row):
            style_key = (
                "table_first_col"
                if (col_idx == 0 and highlight_first_col)
                else "table_cell"
            )
            cells.append(Paragraph(str(cell), styles[style_key]))
        # Pad short rows
        while len(cells) < n_cols:
            cells.append(Paragraph("", styles["table_cell"]))
        table_data.append(cells)

    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
    ]
    if headers:
        style_cmds.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
        style_cmds.append(("TOPPADDING", (0, 0), (-1, 0), 5))
        style_cmds.append(("BOTTOMPADDING", (0, 0), (-1, 0), 5))
    if highlight_first_col:
        style_cmds.append(("BACKGROUND", (0, 1 if headers else 0), (0, -1), LIGHT_GREY))

    col_width = page_width / n_cols
    tbl = Table(table_data, colWidths=[col_width] * n_cols, repeatRows=1 if headers else 0)
    tbl.setStyle(TableStyle(style_cmds))
    story.append(tbl)
    return story


_BLOCK_RENDERERS = {
    "card": lambda b, s, w: _render_card(b, s, w),
    "sections": lambda b, s, w: _render_sections(b, s),
    "numbered": lambda b, s, w: _render_numbered(b, s),
    "table": lambda b, s, w: _render_table(b, s, w),
}


# ---------------------------------------------------------------------------
# Top-level render
# ---------------------------------------------------------------------------

def render(content: dict[str, Any], output_path: str) -> str:
    """Render `content` to a PDF at `output_path`. Returns the absolute output path."""
    regular, bold = register_fonts()
    styles = _make_styles(regular, bold)

    today = datetime.date.today().isoformat()
    footer_id = content.get("footer_id", "")
    sources = content.get("sources", [])
    footer_text = " · ".join(
        s for s in [
            f"Generated {today}",
            footer_id,
            f"sources: {', '.join(sources)}" if sources else "",
        ] if s
    )

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont(regular, 7)
        canvas.setFillColor(GREY)
        canvas.drawString(0.75 * inch, 0.5 * inch, footer_text)
        canvas.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"{doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.85 * inch,
        title=content.get("title", "Snapshot"),
        author="analysis-snapshot-pdf skill",
    )

    page_width = letter[0] - doc.leftMargin - doc.rightMargin
    story: list = []

    # Title + subtitle
    if content.get("title"):
        story.append(Paragraph(content["title"], styles["title"]))
    if content.get("subtitle"):
        story.append(Paragraph(content["subtitle"], styles["subtitle"]))

    # Metadata block (2-column key/value)
    metadata = content.get("metadata") or []
    if metadata:
        meta_rows = [
            [
                Paragraph(label, styles["meta_label"]),
                Paragraph(value, styles["meta_value"]),
            ]
            for label, value in metadata
        ]
        meta_table = Table(meta_rows, colWidths=[1.4 * inch, page_width - 1.4 * inch])
        meta_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 6))

    # Body blocks
    for block in content.get("blocks") or []:
        btype = block.get("type")
        renderer = _BLOCK_RENDERERS.get(btype)
        if renderer is None:
            raise ValueError(f"Unknown block type: {btype!r}")
        story.extend(renderer(block, styles, page_width))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return os.path.abspath(output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main() -> None:
    p = argparse.ArgumentParser(
        description="Render a structured analysis snapshot to PDF.",
    )
    p.add_argument("--input", "-i", required=True, help="Path to JSON content file.")
    p.add_argument("--output", "-o", required=True, help="Path to output PDF.")
    args = p.parse_args()

    with open(args.input) as f:
        content = json.load(f)
    out = render(content, args.output)
    size = os.path.getsize(out)
    print(f"Wrote {out} ({size:,} bytes)")


if __name__ == "__main__":
    _main()
