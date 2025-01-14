import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def scroll_and_load(driver, tile_xpath, max_scroll_attempts=10, delay=3):
    """
    Scrolls the page to load all tiles dynamically.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        tile_xpath (str): XPATH for the tiles to check if loading is complete.
        max_scroll_attempts (int): Maximum number of scroll attempts.
        delay (int): Delay in seconds between scrolls.

    Returns:
        list: List of WebElements representing the loaded tiles.
    """
    last_count = 0
    scroll_attempts = 0
    while scroll_attempts < max_scroll_attempts:
        # Find all tiles on the page
        tiles = driver.find_elements(By.XPATH, tile_xpath)

        # Break if no new tiles are loaded
        if len(tiles) == last_count:
            break

        last_count = len(tiles)
        scroll_attempts += 1

        # Scroll to the last tile
        if tiles:
            ActionChains(driver).move_to_element(tiles[-1]).perform()

        # Wait for new tiles to load
        time.sleep(delay)

    return tiles
