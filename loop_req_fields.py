for row in range(ws.max_row, 1, -1):  # Skip header (row 1)
    cell_value = ws[f"A{row}"].value
    if cell_value not in required_fields:
        ws.delete_rows(row)
