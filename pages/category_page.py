from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .details_page import process_hybrid_page
from utils.utility_func import extract_map_info, extract_property_info
from utils.utility_func import get_total_tiles_count
from utils.utility_func import get_random_category_url
from utils.utility_func import is_category_page
from .base_page import BasePage
import time
import random
from utils.utility_func import generate_comparison_report, xpaths_for_category


class CategoryPage(BasePage):

    def __init__(self, driver):

        super().__init__(driver)
        self.paths = xpaths_for_category()
        self.wait = WebDriverWait(driver, 5)  # Default wait time of 20 seconds

    def navigate_to(self, url):
        """
        Navigate to a specific URL and wait for page load.
        """
        try:
            self.driver.get(url)
            self.wait.until(
                lambda driver: driver.execute_script(
                    'return document.readyState') == 'complete'
            )
            time.sleep(1)  # Additional wait for any dynamic content
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            raise

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
        raise Exception(f"Unable to find a valid Category Page after {
                        max_attempts} attempts.")

    def get_total_tiles(self):
        """
        Retrieve the total number of tiles on the page.
        """
        return get_total_tiles_count(self.driver)

    def wait_for_tiles_container(self):
        """Wait for the main tiles container to be present and visible."""
        try:
            container = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.paths['tile_container']))
            )
            self.wait.until(EC.visibility_of(container))
            return container
        except Exception as e:
            print(f"Error waiting for tiles container: {e}")
            return None

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
            if not container:
                raise Exception("Tiles container not found")

            while len(loaded_tiles) < total_tiles and attempts < max_attempts:
                self.driver.execute_script(
                    "arguments[0].scrollTo({top: arguments[0].scrollHeight, behavior: 'smooth'});",
                    container
                )
                time.sleep(scroll_pause_time)
                loaded_tiles = container.find_elements(
                    By.XPATH,
                    self.paths['property_tile']
                )

                if len(loaded_tiles) == last_count:
                    attempts += 1
                    scroll_pause_time += 0
                else:
                    last_count = len(loaded_tiles)
                    attempts = 0
                    scroll_pause_time = 0.3

                print(f"Loaded {len(loaded_tiles)} of {total_tiles} tiles...")

            print(f"Finished loading tiles. Total loaded: {len(loaded_tiles)}")
            self.driver.execute_script(
                "window.scrollTo({top: 0, behavior: 'smooth'});")
            time.sleep(0.3)
            return loaded_tiles
        except Exception as e:
            print(f"Error loading property tiles: {e}")
            return []

    def process_tiles_randomly_one_by_one(self, all_tiles, url, count=10):
        """
        Process random tiles with improved visibility handling.
        """
        processed_indices = set()
        results = []

        num_tiles = min(len(all_tiles), count)
        print(f"Starting to process {num_tiles} random tiles...")

        for i in range(num_tiles):
            while True:
                random_index = random.randint(0, len(all_tiles) - 1)
                if random_index not in processed_indices:
                    processed_indices.add(random_index)
                    break

            tile = all_tiles[random_index]
            print(f"\nProcessing tile {
                  i + 1}/{num_tiles} (index: {random_index})")

            try:
                self.scroll_to_tile(tile)
                time.sleep(1)

                try:
                    data = self.process_tile(tile, url, wait_time=1, retries=3)
                    if data:
                        results.append({
                            'index': random_index,
                            'data': data
                        })
                        print(f"Successfully processed tile {
                              i + 1}/{num_tiles}")
                except Exception as e:
                    print(f"Error processing tile {random_index}: {e}")

                time.sleep(random.uniform(0.5, 1))
            except Exception as e:
                print(f"Error with tile {random_index}: {e}")
                continue
        return results

    def scroll_to_tile(self, tile):
        """
        Simplified scroll method to bring tile into view.
        """
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", tile)

            self.driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(1)
        except Exception as e:
            print(f"Error scrolling to tile: {e}")

    def process_tile(self, tile, url, wait_time=1, retries=3):
        """
        Enhanced tile processing with comparison to map data and better error handling.

        Args:
            tile (WebElement): The tile element.
            wait_time (int): Maximum time to wait for elements.
            retries (int): Number of retries for processing.

        Returns:
            dict: A dictionary containing tile data, map data, and comparison results.

        Raises:
            Exception: If processing fails after the specified retries.
        """
        attempt = 0
        while attempt < retries:
            try:
                wait = WebDriverWait(self.driver, wait_time)
                tile_data = extract_property_info(tile, wait_time)
                if not tile_data:
                    raise Exception("No data extracted from tile")
                print(f"Successfully extracted tile info: {tile_data}")
                map_data = {}

                try:
                    if self.click_map_icon(tile):
                        self.wait_for_map_to_load()
                        time.sleep(0.5)
                        map_data = extract_map_info(self.driver, wait_time)
                        print(f"Successfully extracted map info: {map_data}")

                except Exception as map_error:
                    print(f"Map interaction failed or map data extraction issue: {
                          map_error}")
                 # Navigate to and extract data from the hybrid page
                hybrid_data = {}
                try:
                    hybrid_data = process_hybrid_page(
                        self.driver, tile, wait_time)
                    print(f"Successfully extracted hybrid page info: {
                          hybrid_data}")
                except Exception as hybrid_error:
                    print(f"Hybrid page interaction failed or data extraction issue: {
                          hybrid_error}")

                generate_comparison_report(
                    tile_data, map_data, hybrid_data, url)
                return {
                    'tile_data': tile_data,
                    'map_data': map_data,
                    'hybrid_data': hybrid_data,
                }

            except Exception as e:
                print(f"Attempt {attempt + 1} failed for tile: {e}")
                attempt += 1
                if attempt < retries:
                    time.sleep(3)
                    self.scroll_to_tile(tile)
                    time.sleep(3)
        raise Exception(f"Failed to process tile after {retries} attempts.")

    def click_map_icon(self, tile):
        """
       Enhanced map icon interaction.
       """
        try:
            selector = self.paths['map_icon']  # Use self.paths
            wait = WebDriverWait(tile, 1)
            map_icon = wait.until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
            ActionChains(self.driver).move_to_element(
                map_icon).click().perform()
            print(f"Map icon clicked successfully using selector: {selector}")
            return True
        except Exception as e:
            print(f"Error clicking map icon: {e}")
            return False

    def wait_for_map_to_load(self, timeout=0.5):

        try:
            wait = WebDriverWait(self.driver, timeout)
            selector = self.paths['map_section']  # Use self.paths
            wait.until(EC.presence_of_element_located((By.XPATH, selector)))
            print("Map section loaded successfully.")
            return
        except Exception as e:
            print(f"Error waiting for map section to load: {e}")
            print("Map section not found with the selector.")

    def scroll_to_specific_tiles(self, all_tiles, tile_indices, smooth=True):
        """
        Scroll to specific tiles by their indices without processing them.
        """
        scrolled_tiles = []
        for index in tile_indices:
            if index < 0 or index >= len(all_tiles):
                print(f"Invalid tile index: {index}")
                continue

            try:
                tile = all_tiles[index]
                print(f"\nScrolling to tile {index}")
                if smooth:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        tile
                    )
                else:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});",
                        tile
                    )
                time.sleep(0.2 if smooth else 0.5)
                self.driver.execute_script("window.scrollBy(0, -100);")
                time.sleep(0.1)

                time.sleep(random.uniform(0.2, 0.5))
            except Exception as e:
                print(f"Error scrolling to tile {index}: {e}")
                continue
        return scrolled_tiles

    def scroll_smoothly_to_bottom(self, pause_time=0.5):
        """
        Smoothly scrolls the page from top to bottom.
        
        Args:
            pause_time (float): Time to wait between scroll increments.
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down by a small increment
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(pause_time)
            
            # Calculate new scroll height and compare
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Stop scrolling when the bottom is reached
            
            last_height = new_height


