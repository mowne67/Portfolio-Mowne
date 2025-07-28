header = [ws.cell(row=1, column=col).value for col in range(1, ws.max_column + 1)]

# Build a dictionary mapping value in column A -> entire row values
row_data_map = {}
for row in range(2, ws.max_row + 1):
    key = ws[f"A{row}"].value
    if key:
        row_data_map[key] = [ws.cell(row=row, column=col).value for col in range(1, ws.max_column + 1)]

# Clear existing data (excluding header)
ws.delete_rows(2, ws.max_row)

# Reinsert rows in the order of required_fields
for i, key in enumerate(required_fields, start=2):
    if key in row_data_map:
        row_values = row_data_map[key]
        for j, value in enumerate(row_values, start=1):
            ws.cell(row=i, column=j).value = value
