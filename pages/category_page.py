from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.random_selector import select_random_elements
from utils.extract_info import extract_property_info
from utils.scroll_helper import scroll_and_load
from utils.page_data_utils import get_total_tiles_count
from utils.url_helper import get_random_category_url
from utils.page_checker import is_category_page
from .base_page import BasePage
import time


class CategoryPage(BasePage):
    """
    Represents the Category Page and provides methods to interact with it.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = {
            'property_tiles': '//div[contains(@class, "property-tiles")]',
            'map_section': '//div[@id="map-info-window"]',  # Example map section ID; adjust based on actual HTML
            'map_content': '//div[@class="map-content"]'  # Adjust to target specific content in the map section
        }

    def navigate_to_valid_category_page(self, max_attempts=10):
        """
        Navigate to a valid Category Page. Retry if the page is invalid.

        Args:
            max_attempts (int): Maximum number of retries to generate a valid page.

        Returns:
            str: The valid URL navigated to.

        Raises:
            Exception: If no valid page is found after max_attempts.
        """
        attempts = 0
        while attempts < max_attempts:
            url = get_random_category_url()
            self.navigate_to(url)

            if is_category_page(self.driver):
                print(f"Valid Category Page found: {url}")
                return url

            print(f"Invalid page detected: {url}. Retrying...")
            attempts += 1

        raise Exception("Unable to find a valid Category Page after maximum attempts.")

    def get_total_tiles(self):
        """
        Retrieve the total number of tiles on the page using a utility function.

        Returns:
            int: Total number of tiles on the page.
        """
        return get_total_tiles_count(self.driver)

    def get_all_property_tiles(self, total_tiles):
        """
        Retrieve all property tiles within the specified container.

        Args:
            total_tiles (int): Total number of tiles to load.

        Returns:
            list: List of WebElements representing the loaded tiles.
        """
        container_xpath = '//div[@id="js-section-0-tiles"]'
        tiles_xpath = './/div[contains(@class, "js-property-tile")]'

        # Locate the container element
        container_element = self.driver.find_element(By.XPATH, container_xpath)
        return scroll_and_load(self.driver, tiles_xpath, total_tiles, container=container_element)

    def get_random_property_tiles(self, all_tiles, count=10):
        """ 
        Get a random subset of property tiles.

        Args:
            all_tiles (list): List of all loaded tiles.
            count (int): Number of random tiles to select.

        Returns:
            list: Randomly selected property tiles.
        """
        tile_count = min(len(all_tiles), count)
        print(f"Found {len(all_tiles)} tiles, selecting {tile_count} random tiles.")
        return select_random_elements(all_tiles, tile_count)

    def process_tile(self, tile, wait_time=20, retries=3):
        """
        Process a single tile, including extracting info and interacting with the map icon.

        Args:
            tile (WebElement): The tile element.
            wait_time (int): Maximum time to wait for elements to load.
            retries (int): Number of retries allowed for each tile.

        Returns:
            dict: Dictionary containing property data.

        Raises:
            Exception: If processing fails after all retries.
        """
        attempt = 0
        while attempt < retries:
            try:
                # Extract tile info
                data = extract_property_info(tile, wait_time)
                print(f"Successfully extracted tile info: {data}")

                # Interact with the map icon
                if self.click_map_icon(tile):
                    print("Map icon interaction successful.")
                    self.wait_for_map_to_load()
                else:
                    print("Failed to interact with the map icon.")

                return data
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for tile: {e}")
                attempt += 1
                time.sleep(2)  # Wait before retrying

        raise Exception(f"Failed to process tile after {retries} attempts.")

    def click_map_icon(self, tile):
        """
        Clicks the map icon for a given tile and verifies the action.

        Args:
            tile (WebElement): The tile element.

        Returns:
            bool: True if the map icon was clicked successfully, False otherwise.
        """
        try:
            # Wait for the map icon to be present and interactable
            wait = WebDriverWait(tile, 10)
            map_icon = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, './/svg[@class="icon"]/*[local-name()="use" and contains(@xlink:href, "#map-marker-solid-icon-v1")]')
                )
            )
            ActionChains(tile.parent).move_to_element(map_icon).click(map_icon).perform()
            print("Map icon clicked successfully.")
            return True
        except Exception as e:
            print(f"Error clicking map icon: {e}")
            return False

    def wait_for_map_to_load(self, timeout=15):
        """
        Waits for the map section to load fully.

        Args:
            timeout (int): Maximum time to wait for the map section to load.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((By.XPATH, self.locators['map_section'])))
            wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['map_content'])))
            print("Map section loaded successfully.")
        except Exception as e:
            print(f"Error waiting for map section to load: {e}")
