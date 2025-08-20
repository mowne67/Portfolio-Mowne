from openpyxl import load_workbook

def reorder_rows_in_app_sheets(file_path: str, required_fields: list[str]) -> None:
    wb = load_workbook(file_path)

    for ws in wb.worksheets:
        if not ws.title.startswith("App"):
            continue

        # Step 1: Build mapping from field name (col A) to full row values
        field_to_row = {}
        for row in range(2, ws.max_row + 1):  # skip header row
            key = ws.cell(row=row, column=1).value
            if key:
                field_to_row[key] = [
                    ws.cell(row=row, column=col).value
                    for col in range(1, ws.max_column + 1)
                ]

        # Step 2: Delete existing data rows (not header)
        ws.delete_rows(2, ws.max_row)

        # Step 3: Reinsert rows in required_fields order
        current_row = 2
        for field in required_fields:
            row_values = field_to_row.get(field, [field] + [""] * (ws.max_column - 1))
            for col_index, value in enumerate(row_values, start=1):
                ws.cell(row=current_row, column=col_index).value = value
            current_row += 1

    wb.save(file_path)
