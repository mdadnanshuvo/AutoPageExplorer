# utils/excel_utils.py
import pandas as pd

def read_excel(file_path, sheet_name):
    """
    Reads an Excel sheet into a DataFrame.
    
    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str): The name of the sheet to read.
    
    Returns:
        DataFrame: The content of the specified sheet.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name)

def get_locators(locator_file):
    """
    Reads locators from the specified Excel file.
    
    Args:
        locator_file (str): The path to the locators Excel file.
    
    Returns:
        dict: A dictionary of locators where keys are locator names and values are the locator values.
    """
    df = read_excel(locator_file, "Locators")
    return df.set_index('name')['locator'].to_dict()

def get_test_data(test_data_file):
    """
    Reads test data from the specified Excel file.
    
    Args:
        test_data_file (str): The path to the test data Excel file.
    
    Returns:
        dict: A dictionary of test data where keys are column names and values are lists of column values.
    """
    df = read_excel(test_data_file, "TestData")
    return df.to_dict(orient='list')