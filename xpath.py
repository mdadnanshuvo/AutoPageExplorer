import re
import pandas as pd


def xpaths_for_category():
    xpaths_file = 'data/xpaths.xlsx'
# Make sure the 'base_url' is set as index
    xpaths_df = pd.read_excel(xpaths_file, index_col=0)

    page_type = 'Category'
    page_xpaths = xpaths_df.loc[xpaths_df['page_type'] == page_type].iloc[0]

    return page_xpaths


print(xpaths_for_category())
