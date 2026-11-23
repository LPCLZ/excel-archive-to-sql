from pathlib import Path
import json
import hashlib
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.utils.cell import coordinate_from_string, get_column_letter

def build_merged_sources(merged_records):
    source_lookup = {}
    for merged_record in merged_records:
        merged_range = CellRange(merged_record["range"])
        for row_number, column_number in merged_range.cells:
            coordinate = f"{get_column_letter(column_number)}{row_number}"
            source_lookup[coordinate] = merged_record["top_left"]
    return source_lookup

def prepare_cells(cell_records, cells_by_coordinate, merged_sources):
    prepared = []
    for record in cell_records:
        coordinate = record["coordinate"]
        source_coordinate = merged_sources.get(coordinate, coordinate)
        source_record = cells_by_coordinate[source_coordinate]
        prepared_record = {
            "coordinate": coordinate,
            "source_coordinate": source_coordinate,
            "raw_value": record["value"],
            "resolved_value": source_record["value"],
            "hyperlink_target": source_record["hyperlink_target"],
            "hyperlink_location": source_record["hyperlink_location"],
        }
        prepared.append(prepared_record)
    return prepared


def group_cells_by_row(cell_records):
    grouped_rows = {}
    for record in cell_records:
        column, row_number = coordinate_from_string(record["coordinate"])
        if row_number not in grouped_rows:
            grouped_rows[row_number] = {}
        grouped_rows[row_number][column] = record
    return grouped_rows

json_path = Path("C:/Users/Liviu/AB-Energy-Code/data/archive_full.json")

reviewed_source_hash = "0643737706a77608a9961c64547d664440d9abfeff0d90c83b515158c7497d4d"
current_source_hash = hashlib.sha256(json_path.read_bytes()).hexdigest()
if current_source_hash != reviewed_source_hash:
    raise ValueError("Source JSON changed. Review project links before continuing.")

with json_path.open("r", encoding="utf-8") as input_file:
    archive_data = json.load(input_file)

print("Worksheet:", archive_data["sheet_name"])

# Organize cell records by their excel addresses.
cells_by_coordinate = {}

for record in archive_data["cells"]:
    cells_by_coordinate[record["coordinate"]] = record

print("Indexed cells:", len(cells_by_coordinate))

merged_sources = build_merged_sources(archive_data["merged_ranges"])

prepared_cells = prepare_cells(archive_data["cells"], cells_by_coordinate, merged_sources)

print("Prepared cells:", len(prepared_cells))

prepared_data = {
    "source_file": archive_data["source_file"],
    "source_json": json_path.name,
    "sheet_name": archive_data["sheet_name"],
    "cell_range": archive_data["cell_range"],
    "cells": prepared_cells,
}

rows = group_cells_by_row(prepared_cells)

print("Rows grouped:", len(rows))

column_map = {
    "A": "unlabeled_a",
    "B": "project_text",
    "C": "beneficiary_text",
    "D": "beneficiary_ab_contracts",
    "E": "operator_beneficiary_contracts",
    "F": "operator_ab_inteligent_ss_contracts",
    "G": "operator_invoices",
    "H": "client_invoices_h",
    "I": "client_invoices_i",
    "J": "unlabeled_j",
}

# Named reords for every excel row.
named_rows = []

for row_number, row_cells in rows.items():
    fields = {}
    for column, cell_record in row_cells.items():
        field_name = column_map[column]
        fields[field_name] = cell_record
    row_record = {
        "source_row": row_number,
        "fields": fields,
    }
    named_rows.append(row_record)

print("Named rows:", len(named_rows))

named_rows_data = {
    "source_file": prepared_data["source_file"],
    "source_json": json_path.name,
    "sheet_name": prepared_data["sheet_name"],
    "cell_range": prepared_data["cell_range"],
    "column_map": column_map,
    "rows": named_rows,
}

# Identify header rows and rows with no values or hyperlinks.
header_row_numbers = [2,3]
blank_row_numbers = []

for named_row in named_rows_data["rows"]:
    is_blank = True
    for cell_record in named_row["fields"].values():
        if (
            cell_record["resolved_value"] is not None
            or cell_record["hyperlink_target"] is not None
            or cell_record["hyperlink_location"] is not None
        ):
            is_blank = False
            break
    if is_blank:
        blank_row_numbers.append(named_row["source_row"])

print("Header rows:", header_row_numbers)
print("Blank rows:", len(blank_row_numbers))

# Collect non_header, nonblank rows for review.
review_rows = []

for named_row in named_rows_data["rows"]:
    row_number = named_row["source_row"]
    if row_number not in header_row_numbers and row_number not in blank_row_numbers:
        review_rows.append(named_row)

print("Rows for review:", len(review_rows))

project_link_overrides = {
    6: ["B4", "B5"],
    20: ["B14"],
    301:["B300"],
}

# Attach reviewed project links while preserving the original fields/
linked_rows = []
for named_row in review_rows:
    row_number = named_row["source_row"]
    linked_row = named_row.copy()
    linked_row["project_sources"] = project_link_overrides.get(row_number)
    linked_rows.append(linked_row)

# Build camdidate groups using confirmed links or project source cells.
candidate_groups = {}
unassigned_rows = []

for linked_row in linked_rows:
    row_number = linked_row["source_row"]
    project_sources = linked_row["project_sources"]
    if project_sources is None:
        project_cell = linked_row["fields"]["project_text"]
        project_text = project_cell["resolved_value"]
        if not isinstance(project_text, str) or not project_text.strip():
            unassigned_rows.append(row_number)
            continue
        project_sources = [project_cell["source_coordinate"]]
    for project_source in project_sources:
        if project_source not in candidate_groups:
            candidate_groups[project_source] = []
        candidate_groups[project_source].append(row_number)

print("Candidate groups:", len(candidate_groups))
print("Unassigned rows:", unassigned_rows)

# Save linked rows with their source metadata.
linked_rows_data = named_rows_data.copy()
linked_rows_data["rows"] = linked_rows
linked_rows_data["candidate_groups"] = candidate_groups
linked_rows_data["unassigned_rows"] = unassigned_rows

linked_output_path = json_path.with_name("archive_linked_rows.json")

with linked_output_path.open("w", encoding="utf-8") as linked_output_file:
    json.dump(linked_rows_data, linked_output_file, ensure_ascii=False, indent=2)

print("Linked rows JSON saved to:", linked_output_path)

# Reopen the linked rows JSON and compare its contents.
with linked_output_path.open("r", encoding="utf-8") as linked_input_file:
    loaded_linked_rows_data = json.load(linked_input_file)

if loaded_linked_rows_data != linked_rows_data:
    raise ValueError("Final JSON verification failed: saved data does not match.")

print("Reloaded linked rows:", len(loaded_linked_rows_data["rows"]))
print("Final JSON verification passed.")
