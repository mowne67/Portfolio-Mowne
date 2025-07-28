# Step 1: Transpose the existing sheet (rows → columns)
transposed = []
for col in range(1, ws.max_column + 1):
    transposed.append([ws.cell(row=row, column=col).value for row in range(1, ws.max_row + 1)])

# Step 2: First column now contains the field names ("Information") — header in index 0
fields = [col[0] for col in transposed[1:]]  # Skip column A (header)

# Map: field name → full column (i.e., original row)
field_to_column = {col[0]: col for col in transposed[1:]}  # exclude header row

# Step 3: Rebuild transposed data: header column first
new_transposed = [transposed[0]]  # First column (A) remains unchanged (e.g., Reference Number, Date, etc.)

# Reorder rest of the columns (i.e., original rows) by required_fields
for field in required_fields:
    if field in field_to_column:
        new_transposed.append(field_to_column[field])
    else:
        # Add empty row if field not found
        new_transposed.append([field] + [""] * (len(transposed[0]) - 1))

# Step 4: Transpose back to row-wise data
final_data = list(zip(*new_transposed))  # Columns → rows

# Step 5: Clear existing sheet
ws.delete_rows(1, ws.max_row)

# Step 6: Write reordered data back
for i, row in enumerate(final_data, start=1):
    for j, value in enumerate(row, start=1):
        ws.cell(row=i, column=j, value=value)
