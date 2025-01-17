import pandas as pd

def generate_comparison_report(domain, url, page, test_case, tile_data, map_data, hybrid_data):
    """
    Compares data from three dictionaries and generates an Excel report with the results.

    Parameters:
        domain (str): Domain name (e.g., "https://www.varoom.com/").
        url (str): Category page URL.
        page (str): Page name (e.g., "Category").
        test_case (str): Formal test case name.
        tile_data (dict): First data source.
        map_data (dict): Second data source.
        hybrid_data (dict): Third data source.

    Returns:
        None. Saves an Excel file named 'comparison_report.xlsx'.
    """
    # Prepare the comparison results
    comparison_results = []

    # Ensure keys are consistent across all dictionaries
    keys = set(tile_data.keys()).union(map_data.keys()).union(hybrid_data.keys())

    for key in keys:
        tile_value = tile_data.get(key, None)
        map_value = map_data.get(key, None)
        hybrid_value = hybrid_data.get(key, None)

        passed = tile_value == map_value == hybrid_value

        comparison_results.append({
            "Key": key,
            "Tile Info": tile_value,
            "Map Info": map_value,
            "Details Info": hybrid_value,
            "Passed": passed
        })

    # Convert to DataFrame
    df = pd.DataFrame(comparison_results)

    # Add metadata columns
    df.insert(0, "Domain", domain)
    df.insert(1, "URL", url)
    df.insert(2, "Page", page)
    df.insert(3, "Test Case", test_case)

    # Save to Excel
    output_file = "comparison_report.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Comparison report saved to {output_file}")




