# Excel Archive to SQL

This is a work-in-progress project using Python and PostgreSQL to turn an Excel contract archive into structured, traceable data.

## Ultimate objective of the project

Build an assistant that answers natural-language questions through WhatsApp about projects, contracts, invoices and payments using a structured SQL database and providing links to the original documents.

## What currently works

- Extracting a worksheet using openpyxl.
- Preserving cell values, coordinates, hyperlinks and merged ranges.
- Resolving merged cells while keeping their original source of information.
- Organizing cells into rows with meaningful field names.
- Building candidate project groups with manually reviewed exceptions.
- Keeping unresolved rows available for further review.
- Saving the prepared data to JSON and verifying it after reloading.

## Database

The repository includes a draft PostgreSQL schema and an example query.
Database import is not implemented yet.

## Current limitations

The scripts currently use local Windows paths and a reviewed archive snapshot. Updated archives require another review of project mappings.

Real company data, documents and generated JSON files are excluded.
A fictional example dataset and portable setup instructions are planned.

## Learning focus

Python functions, dictionaries, file handling, data validation, relational database design and Git version control.