import os
import pandas as pd

def generate_comparison_report( tile_data, map_data, hybrid_data, url, domain = "www.varoom.com",page = "Category", test_case = "Test for data consistency"):
    """
    Generates an Excel report verifying the consistency of property details.

    Args:
        domain (str): Domain name (e.g., "https://www.varoom.com/").
        url (str): Category page URL.
        page (str): Page name (e.g., "Category").
        test_case (str): Test case description.
        tile_data (dict): Data from the property tile.
        map_data (dict): Data from the map info window.
        hybrid_data (dict): Data from the details page.

    Returns:
        None. Saves an Excel report in the `data` folder with `test_reports.xlsx` as the file name.
    """
    # Ensure the 'data' directory exists
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # File path for the report
    output_file = os.path.join(output_dir, "test_reports.xlsx")

    # Check consistency
    passed = tile_data == map_data == hybrid_data

    # Format comments with detailed comparison
    comments = {
        "tile_info": tile_data,
        "map_info_window": map_data,
        "details_info": hybrid_data,
    }

    # Create report data
    report_data = [{
        "Key": tile_data.get("_id", "N/A"),  # Assuming "_id" is in tile_data
        "URL": url,
        "Page": page,
        "Test Case": test_case,
        "Passed": passed,
        "Comments": str(comments)  # Convert dictionary to string for readability
    }]

    # Load existing report or create new
    try:
        existing_df = pd.read_excel(output_file)
        df = pd.concat([existing_df, pd.DataFrame(report_data)], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(report_data)

    # Save updated report
    df.to_excel(output_file, index=False)
    print(f"Comparison report updated in {output_file}")
