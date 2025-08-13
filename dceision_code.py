def safe_float(val):
    if val is None:
        return None
    try:
        return float(str(val).replace(',', '').replace('£', '').strip())
    except ValueError:
        return None

# --- Decision column logic ---
# Assuming: fma is column 2, calculation is column 3, decision is column 4
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

for row in range(2, ws.max_row + 1):
    fma_val = ws.cell(row=row, column=2).value
    calc_val = ws.cell(row=row, column=3).value
    decision_cell = ws.cell(row=row, column=4)

    fma_num = safe_float(fma_val)
    calc_num = safe_float(calc_val)

    if fma_num is None or calc_num is None:
        decision_cell.value = None
    else:
        if fma_num > calc_num:
            decision_cell.value = fma_val
        elif fma_num != calc_num:
            decision_cell.value = calc_val
            decision_cell.fill = red_fill
        else:
            decision_cell.value = calc_val
