import pandas as pd


def xpaths_for_hybrid():
    # Load the Excel file
    xpaths_file = 'data/xpaths.xlsx'  # Path to your Excel file
    xpaths_df = pd.read_excel(xpaths_file)

    # Filter rows for page_type = 'Hybrid'
    page_type = 'Hybrid'
    hybrid_xpaths = xpaths_df[xpaths_df['page_type'] == page_type]

    if not hybrid_xpaths.empty:
        # Convert the row to a dictionary and return
        return hybrid_xpaths.iloc[0].to_dict()
    else:
        return "No xpaths found for Hybrid page type."


# Call the function and print the result
path = xpaths_for_hybrid()
print(path['property_title'])
