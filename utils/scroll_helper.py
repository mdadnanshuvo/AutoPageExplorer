from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_and_load(driver, tile_xpath, max_scroll_attempts=20, delay=10):
    """
    Scrolls the page to load all tiles dynamically using smooth scrolling and ensures they are visible.

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

    # Smooth scroll the page and wait for tiles to load
    while scroll_attempts < max_scroll_attempts:
        tiles = driver.find_elements(By.XPATH, tile_xpath)

        # Break if no new tiles are loaded
        if len(tiles) == last_count:
            print(f"Loaded {len(tiles)} tiles after {scroll_attempts} scroll attempts.")
            break

        last_count = len(tiles)
        scroll_attempts += 1

        # Smooth scroll to the last tile
        if tiles:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", tiles[-1])

        # Wait for new tiles to load
        time.sleep(delay)

    # Wait explicitly for all tiles to be visible
    try:
        WebDriverWait(driver, delay * max_scroll_attempts).until(
            EC.presence_of_all_elements_located((By.XPATH, tile_xpath))
        )
        print("All tiles are now visible.")
    except Exception as e:
        print(f"Error waiting for tiles to load: {e}")

    return driver.find_elements(By.XPATH, tile_xpath)
