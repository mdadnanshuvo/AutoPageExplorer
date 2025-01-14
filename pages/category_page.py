from selenium.webdriver.common.by import By
from utils.random_selector import select_random_elements
from utils.extract_info import extract_property_info
from utils.scroll_helper import scroll_and_load
from utils.page_checker import is_category_page
from utils.page_data_utils import get_total_tiles_count  # Import the utility function
from utils.url_helper import get_random_category_url
from .base_page import BasePage


class CategoryPage(BasePage):
    """
    Represents the Category Page and provides methods to interact with it.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = {
            'property_tiles': '//div[contains(@class, "property-tiles")]'
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

    def get_all_property_tiles(self):
        """
        Retrieve all property tiles on the page by dynamically scrolling.

        Returns:
            list: List of WebElements representing the loaded tiles.
        """
        return scroll_and_load(self.driver, self.locators['property_tiles'])

    def get_random_property_tiles(self, count=10):
        """
        Get a random subset of property tiles.

        Args:
            count (int): Number of random tiles to select.

        Returns:
            list: Randomly selected property tiles.
        """
        all_tiles = self.get_all_property_tiles()
        tile_count = min(len(all_tiles), count)  # Dynamically adjust count
        print(f"Found {len(all_tiles)} tiles, selecting {tile_count} random tiles.")
        return select_random_elements(all_tiles, tile_count)

    def process_tile(self, tile, wait_time=10):
        """
        Process a single tile and extract its property data.

        Args:
            tile (WebElement): The tile element.
            wait_time (int): Maximum time to wait for elements to load.

        Returns:
            dict: Dictionary containing property data, or None if extraction fails.
        """
        try:
            data = extract_property_info(tile, wait_time)
            print(f"Successfully processed tile: {data}")
            return data
        except Exception as e:
            print(f"Failed to process tile: {e}")
            return None
