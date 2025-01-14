def get_total_tiles_count(driver):
    """
    Retrieve the total number of tiles using ScriptData.pageData.Items.length.

    Args:
        driver (WebDriver): Selenium WebDriver instance.

    Returns:
        int: Total number of tiles on the page.
    """
    try:
        total_tiles = driver.execute_script("return ScriptData.pageData.Items.length;")
        print(f"Total tiles found: {total_tiles}")
        return total_tiles
    except Exception as e:
        print(f"Error fetching total tiles count: {e}")
        return 0
