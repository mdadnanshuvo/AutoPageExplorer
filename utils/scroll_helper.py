from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_and_load(driver, tiles_xpath, total_tiles, container=None):
    """
    Scrolls and loads elements matching the provided XPath within a specific container.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        tiles_xpath (str): XPath to locate tile elements.
        total_tiles (int): Total number of tiles expected.
        container (WebElement): Optional container element to scope the search.

    Returns:
        list: List of WebElements found.
    """
    loaded_tiles = []
    scroll_attempts = 0
    max_scroll_attempts = 10  # Adjust as necessary

    # Use the container element if provided; otherwise, default to the document body
    search_context = container or driver

    while len(loaded_tiles) < total_tiles and scroll_attempts < max_scroll_attempts:
        loaded_tiles = search_context.find_elements(By.XPATH, tiles_xpath)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", search_context)
        time.sleep(2)  # Allow time for loading
        scroll_attempts += 1

    return loaded_tiles
