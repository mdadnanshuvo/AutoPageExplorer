from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_and_load(driver, tiles_xpath, total_tiles, container=None, center_tiles=False):
    """
    Scrolls and loads elements matching the provided XPath within a specific container.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        tiles_xpath (str): XPath to locate tile elements.
        total_tiles (int): Total number of tiles expected.
        container (WebElement): Optional container element to scope the search.
        center_tiles (bool): Scroll each tile to the center of the viewport if True.

    Returns:
        list: List of WebElements found.
    """
    loaded_tiles = []
    scroll_attempts = 0
    max_scroll_attempts = 20  # Adjust as necessary
    search_context = container or driver

    while len(loaded_tiles) < total_tiles and scroll_attempts < max_scroll_attempts:
        loaded_tiles = search_context.find_elements(By.XPATH, tiles_xpath)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", search_context)
        time.sleep(2)  # Allow time for loading
        scroll_attempts += 1

    if center_tiles:
        for tile in loaded_tiles:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", tile)
            time.sleep(0.5)  # Allow smooth scrolling

    return loaded_tiles
