def highlight_headers(headers):
    return [
        'background-color: red' if col in [
            'Information',
            'Underwriter (calculation that already has been populated on BP filled underwriter)',
            'Comment (UW)'
        ] else ''
        for col in headers
    ]

styled_df = combined_df.style.set_table_styles([
    {
        'selector': 'th',
        'props': [('background-color', 'white')]  # default white for all
    }
])

styled_df = styled_df.set_table_styles(
    [{'selector': f'th.col{i}', 'props': [('background-color', 'red')]}
     for i, col in enumerate(combined_df.columns)
     if col in [
         'Information',
         'Underwriter (calculation that already has been populated on BP filled underwriter)',
         'Comment (UW)'
     ]
    ],
    overwrite=False
)

styled_df.to_excel(writer, index=False, sheet_name=sheet_name, engine="openpyxl")
