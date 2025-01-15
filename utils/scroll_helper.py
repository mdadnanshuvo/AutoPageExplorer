from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scroll_and_load(driver, tiles_xpath, total_tiles, container=None, center_tiles=False, initial_scroll_time=1):
    """
    Dynamically scrolls and loads elements matching the provided XPath within a specific container,
    with an optional initial scrolling time and tile centralization.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        tiles_xpath (str): XPath to locate tile elements.
        total_tiles (int): Total number of tiles expected.
        container (WebElement): Optional container element to scope the search.
        center_tiles (bool): Scroll each tile to the center of the viewport if True.
        initial_scroll_time (int): Time in seconds for initial dynamic scrolling.

    Returns:
        list: List of WebElements found.
    """
    # Perform initial scrolling to allow the page to load dynamically
    start_time = time.time()
    while time.time() - start_time < initial_scroll_time:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1)  # Pause to simulate natural scrolling

    print("Initial scrolling completed. Starting tile loading...")

    # Scroll and load tiles
    loaded_tiles = []
    scroll_attempts = 0
    max_scroll_attempts = 20  # Adjust as necessary

    # Use container if provided, otherwise scroll the document body
    scroll_target = container if container else driver.find_element(By.TAG_NAME, "body")

    while len(loaded_tiles) < total_tiles and scroll_attempts < max_scroll_attempts:
        loaded_tiles = driver.find_elements(By.XPATH, tiles_xpath)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_target)
        time.sleep(2)  # Allow time for loading
        scroll_attempts += 1

    print(f"Loaded {len(loaded_tiles)} tiles after scrolling.")

    # Optionally center each tile in the viewport
    if center_tiles:
        for tile in loaded_tiles:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", tile)
                time.sleep(0.5)  # Allow smooth scrolling
                print("Tile centered.")
            except Exception as e:
                print(f"Error centering tile: {e}")

    return loaded_tiles
