from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Load workbook and sheet
wb = load_workbook("output.xlsx")
ws = wb["Sheet1"]

# Create red fill
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

# Color specific cells by name
for cell_name in ["G1", "E1", "T1"]:
    ws[cell_name].fill = red_fill

# Save the workbook
wb.save("output.xlsx")
