import pandas as pd
import numpy as np
import re

def create_decision(fma_value, calculation_value):
    """
    Compare currency values and return the higher one in original format
    """
    if pd.isna(fma_value) or pd.isna(calculation_value):
        return fma_value if pd.notna(fma_value) else calculation_value
    
    # Currency symbols pattern
    currency_pattern = r'[$€£¥₹₽₩₪₦₨₡₱₫₵₴₸₺₼₾₿¢]'
    
    # Clean and convert to numeric for comparison
    fma_numeric = float(re.sub(currency_pattern, '', str(fma_value)).strip())
    calculation_numeric = float(re.sub(currency_pattern, '', str(calculation_value)).strip())
    
    # Return original string format of the higher value
    return fma_value if fma_numeric > calculation_numeric else calculation_value

# Apply the function to create the decision column
df['decision'] = df.apply(lambda row: create_decision(row['fma'], row['calculation']), axis=1)
