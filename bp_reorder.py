# Step 1: Capture all rows (row 2 onwards) in a dict based on column A (Information)
field_to_row = {}
for row in range(2, ws.max_row + 1):
    key = ws[f"A{row}"].value
    if key:
        field_to_row[key] = [ws.cell(row=row, column=col).value for col in range(1, ws.max_column + 1)]

# Step 2: Delete all rows except the header
ws.delete_rows(2, ws.max_row)

# Step 3: Re-insert rows in the order of required_fields
for i, field in enumerate(required_fields, start=2):
    row_values = field_to_row.get(field, [""] * ws.max_column)  # Empty row if not found
    for j, value in enumerate(row_values, start=1):
        ws.cell(row=i, column=j).value = value
