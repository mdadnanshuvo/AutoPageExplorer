def is_category_page(driver):
    """
    Checks if the current page is a Category Page using the ScriptData.pageLayout variable.

    Args:
        driver (WebDriver): Selenium WebDriver instance.

    Returns:
        bool: True if the page is a Category Page, False otherwise.
    """
    try:
        # Execute JavaScript to get the value of ScriptData.pageLayout
        page_layout = driver.execute_script("return ScriptData.pageLayout;")
        print(f"ScriptData.pageLayout: {page_layout}")  # Debugging output
        return page_layout == "Category"
    except Exception as e:
        print(f"Error while checking ScriptData.pageLayout: {e}")
        return False
