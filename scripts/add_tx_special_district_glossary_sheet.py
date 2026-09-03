#!/usr/bin/env python3
"""
Add a "Special District Key Glossary" sheet to TX_Municipalities.xlsx,
summarizing the type-key registry at reference/TX Rolling Audit/
Special_District_Type_Keys.md (issue #32) so it's visible alongside the
workbook's other sheets, not just in a separate markdown file.

Parses the registry's markdown table live (rather than hardcoding it) so
re-running this script after the registry is updated keeps the sheet in
sync, same "compute live, don't hand-maintain a duplicate" discipline as
add_tx_municipalities_readme_sheet.py's README sheet.

Inserts (or replaces) the sheet right after README. Leaves every other
sheet's cells and formatting untouched.

Usage: python3 add_tx_special_district_glossary_sheet.py [--write]
"""
import re
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.hyperlink import Hyperlink

REPO = Path(__file__).resolve().parent.parent
XLSX_PATH = REPO / "reference" / "TX Rolling Audit" / "TX_Municipalities.xlsx"
REGISTRY_PATH = REPO / "reference" / "TX Rolling Audit" / "Special_District_Type_Keys.md"
REGISTRY_RELATIVE_LINK = "Special_District_Type_Keys.md"  # same folder as the workbook


def parse_markdown_table(md_text, section_heading):
    """Extract rows from the first pipe-table under a given '## heading' (or
    the whole doc if section_heading is None), as a list of cell-lists.
    Skips the header row and the '---' separator row."""
    lines = md_text.splitlines()
    if section_heading:
        start = next(i for i, line in enumerate(lines) if line.strip() == section_heading)
        lines = lines[start:]

    table_lines = [line for line in lines if line.strip().startswith("|")]
    rows = []
    for line in table_lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue  # separator row
        rows.append(cells)
    return rows


def clean_cell(text):
    """Strip markdown emphasis/backticks for a plain-text spreadsheet cell."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def main():
    write = "--write" in sys.argv[1:]

    md_text = REGISTRY_PATH.read_text()
    table_rows = parse_markdown_table(md_text, None)
    header, data_rows = table_rows[0], table_rows[1:]

    wb = openpyxl.load_workbook(XLSX_PATH)

    if "Special District Key Glossary" in wb.sheetnames:
        del wb["Special District Key Glossary"]
    insert_at = wb.sheetnames.index("README") + 1 if "README" in wb.sheetnames else 0
    ws = wb.create_sheet("Special District Key Glossary", insert_at)

    widths = [34, 44, 20, 46, 14, 70]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = w

    title_font = Font(bold=True, size=14)
    header_font = Font(bold=True)
    wrap = Alignment(wrap_text=True, vertical="top")
    link_font = Font(color="0563C1", underline="single")

    ws["A1"] = "TX Special District Jurisdiction Type-Key Registry"
    ws["A1"].font = title_font
    ws.merge_cells("A1:F1")

    ws["A2"] = (
        "Canonical ocd-division/ocd-jurisdiction type keys for TX special-district "
        "entities that don't map 1:1 onto an existing county/place jurisdiction "
        "(issue #32; mirrors the school_district:/appraisal_district: precedent "
        "already in the repo). Full document, including naming rules and the "
        "out-of-scope list, linked below -- this sheet is a summary snapshot, "
        "regenerated from that document, not a separate source of truth."
    )
    ws["A2"].alignment = wrap
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 45

    link_cell = ws["A3"]
    link_cell.value = f"Full document: {REGISTRY_RELATIVE_LINK}"
    link_cell.hyperlink = Hyperlink(ref="A3", target=REGISTRY_RELATIVE_LINK)
    link_cell.font = link_font
    ws.merge_cells("A3:F3")

    header_row = 5
    for i, h in enumerate(header, start=1):
        c = ws.cell(row=header_row, column=i, value=h)
        c.font = header_font

    for i, row in enumerate(data_rows, start=header_row + 1):
        for j, cell_text in enumerate(row, start=1):
            ws.cell(row=i, column=j, value=clean_cell(cell_text)).alignment = wrap
        ws.row_dimensions[i].height = 45

    print(f"Special District Key Glossary sheet built with {len(data_rows)} type-key rows.")
    for row in data_rows:
        print(f"  {row[0]}: {row[-1][:80]}")

    if write:
        wb.save(XLSX_PATH)
        print(f"\nSaved {XLSX_PATH}")
    else:
        print("\n(dry run -- pass --write to save)")


if __name__ == "__main__":
    main()
