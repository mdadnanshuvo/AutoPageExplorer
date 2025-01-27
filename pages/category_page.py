from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from .details_page import process_hybrid_page
from utils.utility_func import (
    extract_map_info,
    extract_property_info,
    get_total_tiles_count,
    get_random_category_url,
    is_category_page,
    generate_comparison_report,
    xpaths_for_category
)
import time


class CategoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.paths = xpaths_for_category()

    def navigate_to_valid_category_page(self, max_attempts=10):
        """
        Navigate to a valid Category Page. Retry if the page is invalid.
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                url = get_random_category_url()
                print(f"Attempting to navigate to: {url}")
                self.navigate_to(url)
                time.sleep(2)

                if is_category_page(self.driver):
                    print(f"Valid Category Page found: {url}")
                    return url

                print(f"Invalid page detected: {url}. Retrying...")
                attempts += 1
                time.sleep(1)
            except Exception as e:
                print(f"Error during navigation attempt {attempts + 1}: {e}")
                attempts += 1
                time.sleep(2)
        raise Exception(f"Unable to find a valid Category Page after {max_attempts} attempts.")

    def get_total_tiles(self):
        """
        Retrieve the total number of tiles on the page.
        """
        return get_total_tiles_count(self.driver)

    def wait_for_tiles_container(self):
        """Wait for the main tiles container to be present and visible."""
        return self.wait_for_element((By.XPATH, self.paths['tile_container']))

    def load_all_property_tiles(self, total_tiles):
        """
        Load all property tiles by scrolling to the bottom.
        """
        print(f"Starting to load all {total_tiles} property tiles...")
        loaded_tiles = []
        last_count = 0
        attempts = 0
        max_attempts = 30
        scroll_pause_time = 0

        try:
            container = self.wait_for_tiles_container()
            while len(loaded_tiles) < total_tiles and attempts < max_attempts:
                self.driver.execute_script(
                    "arguments[0].scrollTo({top: arguments[0].scrollHeight, behavior: 'smooth'});",
                    container
                )
                time.sleep(scroll_pause_time)
                loaded_tiles = self.find_elements((By.XPATH, self.paths['property_tile']))

                if len(loaded_tiles) == last_count:
                    attempts += 1
                    scroll_pause_time += 0
                else:
                    last_count = len(loaded_tiles)
                    attempts = 0
                    scroll_pause_time = 0.3

                print(f"Loaded {len(loaded_tiles)} of {total_tiles} tiles...")

            print(f"Finished loading tiles. Total loaded: {len(loaded_tiles)}")
            return loaded_tiles
        except Exception as e:
            print(f"Error loading property tiles: {e}")
            return []

    def scroll_to_tile(self, tile):
        """
        Scrolls to a specific tile using the base page scroll method.
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", tile)
            self.driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(1)
        except Exception as e:
            print(f"Error scrolling to tile: {e}")

    def click_map_icon(self, tile):
        """
        Clicks the map icon within a tile.
        """
        try:
            map_icon = tile.find_element(By.XPATH, self.paths['map_icon'])
            ActionChains(self.driver).move_to_element(map_icon).click().perform()
            print("Map icon clicked successfully.")
            return True
        except Exception as e:
            print(f"Error clicking map icon: {e}")
            return False

    def wait_for_map_to_load(self, timeout=2.5):
        """
        Waits for the map section to load.
        """
        try:
            self.wait_for_element((By.XPATH, self.paths['map_section']), timeout)
            print("Map section loaded successfully.")
        except Exception as e:
            print(f"Error waiting for map section to load: {e}")

    def process_tile(self, tile, url, wait_time=1):
        """
        Processes a single tile, extracting data and generating a report.
        """
        tile_data = extract_property_info(tile, wait_time)
        if not tile_data:
            raise Exception("Failed to extract data from tile.")
        print(f"Successfully extracted tile info: {tile_data}")

        # Extract map data
        map_data = {}
        if self.click_map_icon(tile):
            self.wait_for_map_to_load()
            time.sleep(1.5)
            map_data = extract_map_info(self.driver, wait_time)
            print(f"Successfully extracted map info: {map_data}")

        # Extract hybrid page data
        hybrid_data = process_hybrid_page(self.driver, tile, wait_time)
        print(f"Successfully extracted hybrid page info: {hybrid_data}")

        # Generate comparison report
        generate_comparison_report(tile_data, map_data, hybrid_data, url)

        return {
            'tile_data': tile_data,
            'map_data': map_data,
            'hybrid_data': hybrid_data,
        }
    