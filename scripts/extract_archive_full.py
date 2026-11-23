from pathlib import Path
from openpyxl import load_workbook
import json

# Store the location of the original excel archive
# Creating a path object does not open the file
archive_path = Path("C:/Users/Liviu/AB-Energy-Code/data/Arhiva contracte - AB Energy.xlsx")

# Continue with extraction if the source path points to an existing file
if archive_path.is_file():
    workbook = load_workbook(archive_path)
    sheet = workbook["Arhiva contracte"]

    cell_records = []

    for row in sheet.iter_rows():
        for cell in row:
            hyperlink_target = None
            hyperlink_location = None

            if cell.hyperlink is not None:
                hyperlink_target = cell.hyperlink.target
                hyperlink_location = cell.hyperlink.location

            cell_info = {
                "coordinate": cell.coordinate,
                "value": cell.value,
                "hyperlink_target": hyperlink_target,
                "hyperlink_location": hyperlink_location,
            }
            cell_records.append(cell_info)    
    print("Cells collected:", len(cell_records))

# Count formula cells across the whole worksheet
    formula_count = 0

    for row in sheet.iter_rows():
        for cell in row:
            if cell.data_type == "f":
                formula_count += 1

    print("Formula cells found:", formula_count)

# Count how many cell values belong to each Python type
    type_counts = {}

    for row in sheet.iter_rows():
        for cell in row:
            value_type = type(cell.value).__name__
            type_counts[value_type] = type_counts.get(value_type, 0) + 1

    print("Value types:", type_counts)

# Record each merged range, its top-left cell, and its value
    merged_records = []
    
    for merged_range in sheet.merged_cells.ranges:
        top_left_cell = sheet.cell(row=merged_range.min_row, column=merged_range.min_col)
        merged_info = {
            "range": str(merged_range),
            "top_left": top_left_cell.coordinate,
            "value": top_left_cell.value,
        }
        merged_records.append(merged_info)

    print("Merged ranges collected:", len(merged_records))

    archive_data = {
        "source_file": archive_path.name,
        "sheet_name": sheet.title,
        "cell_range": sheet.dimensions,
        "cells": cell_records,
        "merged_ranges_scope": "whole_worksheet",
        "merged_ranges": merged_records,
    }
    print("Data ready for JSON")

    output_path = archive_path.with_name("archive_full.json")

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(archive_data, output_file, ensure_ascii=False, indent=2)

    print("JSON saved to:", output_path)

    with output_path.open("r", encoding="utf-8") as input_file:
        loaded_data = json.load(input_file)

    print("Reloaded cells:", len(loaded_data["cells"]))
    print("Reloaded merged ranges:", len(loaded_data["merged_ranges"]))
    print("Data matches:", loaded_data == archive_data)

else:
    print("Archive not found")
