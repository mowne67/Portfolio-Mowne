# Create a new worksheet for reordered data
ordered_ws = wb.create_sheet(title="Reordered")

# Step 1: Copy header from original worksheet
for col in range(1, ws.max_column + 1):
    ordered_ws.cell(row=1, column=col).value = ws.cell(row=1, column=col).value

# Step 2: Build a dictionary from column A (Information) to full row values
field_to_row = {}
for row in range(2, ws.max_row + 1):
    key = ws[f"A{row}"].value
    if key:
        field_to_row[key] = [ws.cell(row=row, column=col).value for col in range(1, ws.max_column + 1)]

# Step 3: Write rows to new sheet in required_fields order
for i, field in enumerate(required_fields, start=2):
    row_values = field_to_row.get(field, [""] * ws.max_column)  # Blank row if not found
    for j, value in enumerate(row_values, start=1):
        ordered_ws.cell(row=i, column=j).value = value
