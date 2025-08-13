import pandas as pd
import numpy as np
import re
from openpyxl import load_workbook
from openpyxl.styles import Font

def clean_currency(value):
    """Remove currency symbols and convert to float"""
    if pd.isna(value) or value == '' or str(value).upper() == 'NA':
        return np.nan
    
    # Convert to string and remove common currency symbols
    clean_val = str(value).strip()
    # Remove currency symbols from both sides
    clean_val = re.sub(r'^[\$£€¥₹]+|[\$£€¥₹]+$', '', clean_val)
    # Remove commas and spaces
    clean_val = re.sub(r'[,\s]', '', clean_val)
    
    try:
        return float(clean_val)
    except ValueError:
        return np.nan

def apply_decision_rules(row):
    """Apply the decision rules for each row"""
    fma_clean = clean_currency(row['fma'])
    calc_clean = clean_currency(row['calculation'])
    
    # If either field is empty/NA, leave blank
    if pd.isna(fma_clean) or pd.isna(calc_clean):
        return {'value': '', 'color': 'black'}
    
    # If fma is higher than calculation, show fma
    if fma_clean > calc_clean:
        return {'value': row['fma'], 'color': 'black'}
    
    # If fma and calculation don't match, show calculation in red
    if fma_clean != calc_clean:
        return {'value': row['calculation'], 'color': 'red'}
    
    # If they match exactly, show the value in black
    return {'value': row['calculation'], 'color': 'black'}

# Read the Excel file
def process_excel_file(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Apply the decision rules
    decisions = df.apply(apply_decision_rules, axis=1)
    
    # Extract values and colors
    df['decision'] = [d['value'] for d in decisions]
    decision_colors = [d['color'] for d in decisions]
    
    # Save to Excel with formatting
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # Find the decision column (assuming it's the last column)
        decision_col = len(df.columns)
        
        # Apply red color formatting where needed
        red_font = Font(color="FF0000")  # Red color
        
        for idx, color in enumerate(decision_colors, start=2):  # start=2 because row 1 is header
            if color == 'red':
                cell = worksheet.cell(row=idx, column=decision_col)
                cell.font = red_font

# Example usage
if __name__ == "__main__":
    # If you want to test with sample data
    sample_data = {
        'fma': ['$100', '€200', '₹150', '', '$300', 'NA', '$250'],
        'calculation': ['$80', '€200', '₹200', '$120', '', '$250', '$250'],
        'underwriter': ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'David', 'Eve']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Apply the decision rules
    decisions = df.apply(apply_decision_rules, axis=1)
    df['decision'] = [d['value'] for d in decisions]
    decision_colors = [d['color'] for d in decisions]
    
    print("Sample result:")
    print(df)
    print("\nColors for decision column:", decision_colors)
    
    # To process your actual Excel file, uncomment and modify these lines:
    # input_file = 'your_input_file.xlsx'
    # output_file = 'your_output_file.xlsx'
    # process_excel_file(input_file, output_file)
