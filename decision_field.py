import pandas as pd
import numpy as np
import re

def create_decision(fma_value, calculation_value):
    """
    Compare currency values and return the higher one in original format
    Handles non-numeric strings by treating them as invalid for comparison
    """
    if pd.isna(fma_value) or pd.isna(calculation_value):
        return fma_value if pd.notna(fma_value) else calculation_value
    
    # Currency symbols pattern
    currency_pattern = r'[$€£¥₹₽₩₪₦₨₡₱₫₵₴₸₺₼₾₿¢]'
    
    def safe_convert_to_numeric(value):
        """Safely convert currency string to numeric, return None if not possible"""
        try:
            cleaned = re.sub(currency_pattern, '', str(value)).strip()
            # Check if the cleaned string contains only digits, decimal points, and minus signs
            if re.match(r'^-?\d*\.?\d*$', cleaned) and cleaned not in ['', '.', '-']:
                return float(cleaned)
            else:
                return None
        except (ValueError, TypeError):
            return None
    
    # Try to convert both values to numeric
    fma_numeric = safe_convert_to_numeric(fma_value)
    calculation_numeric = safe_convert_to_numeric(calculation_value)
    
    # If both are numeric, compare them
    if fma_numeric is not None and calculation_numeric is not None:
        return fma_value if fma_numeric > calculation_numeric else calculation_value
    
    # If only one is numeric, return the numeric one
    elif fma_numeric is not None and calculation_numeric is None:
        return fma_value
    elif fma_numeric is None and calculation_numeric is not None:
        return calculation_value
    
    # If neither is numeric, return fma by default (or you can define your own logic)
    else:
        return fma_value


# Apply the function to create the decision column
df['decision'] = df.apply(lambda row: create_decision(row['fma'], row['calculation']), axis=1)
