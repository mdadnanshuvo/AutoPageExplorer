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
import random


class CategoryPage(BasePage):
    """
    Represents the Category Page and provides methods to interact with it.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = {
            'property_tiles': '//div[contains(@class, "js-tiles-container")]',
            'map_section': '//div[@id="map-info-window"]',
            'map_content': '//div[@class="map-content"]'
        }

    def navigate_to_valid_category_page(self, max_attempts=10):
        """
        Navigate to a valid Category Page. Retry if the page is invalid.
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
        Retrieve the total number of tiles on the page.
        """
        return get_total_tiles_count(self.driver)

    def load_all_property_tiles(self, total_tiles):
        """
        First phase: Load all property tiles by scrolling to the bottom.
        
        Args:
            total_tiles (int): Expected number of tiles to load.
            
        Returns:
            list: List of all loaded tile elements.
        """
        print(f"Starting to load all {total_tiles} property tiles...")
        
        # Initialize variables
        loaded_tiles = []
        last_count = 0
        attempts = 0
        max_attempts = 30  # Maximum scrolling attempts
        
        try:
            # Find the container that holds all tiles
            container = self.driver.find_element(By.XPATH, '//div[@id="js-tiles-container"]')
            
            # Scroll until we've loaded all tiles or reached max attempts
            while len(loaded_tiles) < total_tiles and attempts < max_attempts:
                # Scroll to bottom of container
                self.driver.execute_script(
                    "arguments[0].scrollTo(0, arguments[0].scrollHeight);", 
                    container
                )
                
                # Wait for new content to load
                time.sleep(2)
                
                # Get current tiles
                loaded_tiles = container.find_elements(
                    By.XPATH, 
                    './/div[contains(@class, "js-property-tile")]'
                )
                
                # Check if we've loaded new tiles
                if len(loaded_tiles) == last_count:
                    attempts += 1
                else:
                    last_count = len(loaded_tiles)
                    attempts = 0  # Reset attempts when we find new tiles
                
                print(f"Loaded {len(loaded_tiles)} of {total_tiles} tiles...")
            
            print(f"Finished loading tiles. Total loaded: {len(loaded_tiles)}")
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            return loaded_tiles
            
        except Exception as e:
            print(f"Error loading property tiles: {e}")
            return []

    def process_tiles_randomly_one_by_one(self, all_tiles, count=10):
        """
        Second phase: Process random tiles one by one with centered scrolling.
        
        Args:
            all_tiles (list): List of all loaded tiles.
            count (int): Number of tiles to process.
            
        Returns:
            list: List of processed tile data.
        """
        processed_indices = set()
        results = []
        
        # Calculate number of tiles to process
        num_tiles = min(len(all_tiles), count)
        print(f"Starting to process {num_tiles} random tiles...")
        
        for i in range(num_tiles):
            # Select a random unprocessed tile
            while True:
                random_index = random.randint(0, len(all_tiles) - 1)
                if random_index not in processed_indices:
                    processed_indices.add(random_index)
                    break
            
            tile = all_tiles[random_index]
            print(f"\nProcessing tile {i + 1}/{num_tiles} (index: {random_index})")
            
            try:
                # Center the selected tile
                self.scroll_tile_to_center(tile)
                
                # Wait for tile to be fully visible
                if self.wait_for_tile_visibility(tile):
                    # Process the tile
                    data = self.process_tile(tile)
                    results.append({
                        'index': random_index,
                        'data': data
                    })
                    print(f"Successfully processed tile {i + 1}/{num_tiles}")
                else:
                    print(f"Skipping tile {random_index} - visibility check failed")
                
            except Exception as e:
                print(f"Error processing tile {random_index}: {e}")
                continue
            
            # Random delay between processing tiles
            time.sleep(random.uniform(1.5, 3.0))
        
        return results

    def scroll_tile_to_center(self, tile):
        """
        Scroll a specific tile to the center of the viewport.
        """
        try:
            # Initial scroll to bring element into rough center
            self.driver.execute_script("""
                arguments[0].scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            """, tile)
            
            # Wait for initial scroll
            time.sleep(1)
            
            # Fine-tune the position
            viewport_height = self.driver.execute_script("return window.innerHeight;")
            elem_position = tile.location['y']
            
            # Calculate center position
            ideal_scroll = elem_position - (viewport_height / 2) + (tile.size['height'] / 2)
            
            # Adjust if needed
            self.driver.execute_script(
                "window.scrollTo({top: arguments[0], behavior: 'smooth'});", 
                ideal_scroll
            )
            
            # Wait for final positioning
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error centering tile: {e}")

    def wait_for_tile_visibility(self, tile, timeout=10):
        """
        Ensure tile is fully visible and loaded.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            # Check basic visibility
            wait.until(EC.visibility_of(tile))
            
            # Wait for tile to be interactive
            wait.until(lambda d: (
                tile.is_displayed() and
                tile.is_enabled() and
                tile.get_attribute('class') is not None
            ))
            
            # Verify tile is in viewport
            is_in_viewport = self.driver.execute_script("""
                var elem = arguments[0];
                var rect = elem.getBoundingClientRect();
                return (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                );
            """, tile)
            
            return is_in_viewport
            
        except Exception as e:
            print(f"Error checking tile visibility: {e}")
            return False

    def process_tile(self, tile, wait_time=20, retries=3):
        """Process a single tile with retries."""
        attempt = 0
        while attempt < retries:
            try:
                # Extract tile info
                data = extract_property_info(tile, wait_time)
                print(f"Successfully extracted tile info: {data}")

                # Interact with map icon
                if self.click_map_icon(tile):
                    print("Map icon interaction successful.")
                    self.wait_for_map_to_load()
                else:
                    print("Failed to interact with map icon.")

                return data
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for tile: {e}")
                attempt += 1
                time.sleep(2)

        raise Exception(f"Failed to process tile after {retries} attempts.")

    def click_map_icon(self, tile):
        """Click the map icon for a tile."""
        try:
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
        """Wait for map section to load."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((By.XPATH, self.locators['map_section'])))
            wait.until(EC.visibility_of_element_located((By.XPATH, self.locators['map_content'])))
            print("Map section loaded successfully.")
        except Exception as e:
            print(f"Error waiting for map section to load: {e}")