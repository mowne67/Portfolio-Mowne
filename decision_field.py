import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Read the Excel file
df = pd.read_csv("file.csv") # Replace with your actual file path

# Create the decision column based on your rules
def create_decision(row):
    fma = row['fma']
    calculation = row['calculation']
    
    # Rule 3: If either field is blank/NA, leave decision blank
    if pd.isna(fma) or pd.isna(calculation) or fma == '' or calculation == '':
        return np.nan
    
    # Rule 1: If fma > calculation, show fma
    if fma > calculation:
        return fma
    
    # Rule 2: If fma != calculation (and fma <= calculation), show calculation
    # This will be formatted with red background later
    else:
        return calculation

# Apply the logic to create the decision column
df['decision'] = df.apply(create_decision, axis=1)

# Save to a new Excel file with formatting
output_file = 'output_file.xlsx'
df.to_excel(output_file, index=False)

# Now apply red background formatting to cells where fma != calculation
wb = load_workbook(output_file)
ws = wb.active

# Create red background fill style
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

# Find the decision column index (assuming it's the last column)
decision_col_idx = len(df.columns)

# Apply formatting
for idx, row in df.iterrows():
    fma = row['fma']
    calculation = row['calculation']
    decision = row['decision']
    
    # Skip if decision is blank
    if pd.isna(decision):
        continue
    
    # If fma != calculation and we're showing calculation, make background red
    if not pd.isna(fma) and not pd.isna(calculation) and fma != calculation and fma <= calculation:
        cell = ws.cell(row=idx + 2, column=decision_col_idx)  # +2 because of header and 0-indexing
        cell.fill = red_fill

# Save the formatted file
wb.save(output_file)
print(f"File saved as: {output_file}")
