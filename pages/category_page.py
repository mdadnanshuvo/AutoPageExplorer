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
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = {
            'property_tiles': '//div[contains(@class, "js-tiles-container")]',
            'map_section': '//div[@id="map-info-window"]',
            'map_content': '//div[@class="map-content"]',
            'tile_container': '//div[@id="js-tiles-container"]',
            'property_tile': './/div[contains(@class, "js-property-tile")]'
        }
        self.wait = WebDriverWait(driver, 20)  # Default wait time of 20 seconds

    def navigate_to(self, url):
        """
        Navigate to a specific URL and wait for page load.
        """
        try:
            self.driver.get(url)
            # Wait for DOM to be fully loaded
            self.wait.until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(2)  # Additional wait for any dynamic content
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
                time.sleep(2)  # Wait for page elements to load

                if is_category_page(self.driver):
                    print(f"Valid Category Page found: {url}")
                    return url

                print(f"Invalid page detected: {url}. Retrying...")
                attempts += 1
                time.sleep(1)  # Wait before next attempt
                
            except Exception as e:
                print(f"Error during navigation attempt {attempts + 1}: {e}")
                attempts += 1
                time.sleep(2)  # Wait longer after an error

        raise Exception(f"Unable to find a valid Category Page after {max_attempts} attempts.")

    def get_total_tiles(self):
        """
        Retrieve the total number of tiles on the page.
        """
        return get_total_tiles_count(self.driver)

    def wait_for_tiles_container(self):
        """Wait for the main tiles container to be present and visible."""
        try:
            container = self.wait.until(
                EC.presence_of_element_located((By.XPATH, self.locators['tile_container']))
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
        scroll_pause_time = 3  # Increased pause time between scrolls
        
        try:
            # Wait for container to be ready
            container = self.wait_for_tiles_container()
            if not container:
                raise Exception("Tiles container not found")
            
            while len(loaded_tiles) < total_tiles and attempts < max_attempts:
                # Smooth scroll to bottom
                self.driver.execute_script(
                    "arguments[0].scrollTo({top: arguments[0].scrollHeight, behavior: 'smooth'});", 
                    container
                )
                
                # Wait for scroll animation and content loading
                time.sleep(scroll_pause_time)
                
                # Get current tiles
                loaded_tiles = container.find_elements(
                    By.XPATH, 
                    self.locators['property_tile']
                )
                
                # Check progress
                if len(loaded_tiles) == last_count:
                    attempts += 1
                    scroll_pause_time += 0.5  # Incrementally increase wait time
                else:
                    last_count = len(loaded_tiles)
                    attempts = 0
                    scroll_pause_time = 3  # Reset wait time
                
                print(f"Loaded {len(loaded_tiles)} of {total_tiles} tiles...")
            
            # Final wait for any remaining loading
            time.sleep(2)
            print(f"Finished loading tiles. Total loaded: {len(loaded_tiles)}")
            
            # Smooth scroll back to top
            self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
            time.sleep(2)
            
            return loaded_tiles
            
        except Exception as e:
            print(f"Error loading property tiles: {e}")
            return []

    def process_tiles_randomly_one_by_one(self, all_tiles, count=10):
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
            print(f"\nProcessing tile {i + 1}/{num_tiles} (index: {random_index})")
            
            try:
                # Scroll tile into view with more basic approach
                self.scroll_to_tile(tile)
                time.sleep(2)  # Wait for scroll to complete
                
                # Try to extract data even if visibility check fails
                try:
                    data = self.process_tile(tile, wait_time=30, retries=3)
                    if data:
                        results.append({
                            'index': random_index,
                            'data': data
                        })
                        print(f"Successfully processed tile {i + 1}/{num_tiles}")
                except Exception as e:
                    print(f"Error processing tile {random_index}: {e}")
                
                # Random delay between processing
                time.sleep(random.uniform(2.0, 3.0))
                
            except Exception as e:
                print(f"Error with tile {random_index}: {e}")
                continue
        
        return results

    def scroll_to_tile(self, tile):
        """
        Simplified scroll method to bring tile into view.
        """
        try:
            # Basic scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", tile)
            time.sleep(1)
            
            # Small adjustment to account for any headers
            self.driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(1)
        except Exception as e:
            print(f"Error scrolling to tile: {e}")

    def process_tile(self, tile, wait_time=30, retries=3):
        """
        Enhanced tile processing with better error handling.
        """
        attempt = 0
        while attempt < retries:
            try:
                # Wait for tile to be present in DOM
                wait = WebDriverWait(self.driver, wait_time)
                wait.until(lambda d: tile.is_displayed())
                
                # Extract basic information first
                data = extract_property_info(tile, wait_time)
                if not data:
                    raise Exception("No data extracted from tile")
                
                print(f"Successfully extracted tile info: {data}")

                # Try to interact with map if available
                try:
                    if self.click_map_icon(tile):
                        self.wait_for_map_to_load()
                except Exception as map_error:
                    print(f"Map interaction failed but continuing: {map_error}")

                return data
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for tile: {e}")
                attempt += 1
                if attempt < retries:
                    time.sleep(2)
                    # Try scrolling again
                    self.scroll_to_tile(tile)
                    time.sleep(1)

        raise Exception(f"Failed to process tile after {retries} attempts.")

    def click_map_icon(self, tile):
        """
        Enhanced map icon interaction.
        """
        try:
            # Try multiple selectors for map icon
            selectors = [
                './/svg[@class="icon"]/*[local-name()="use" and contains(@xlink:href, "#map-marker-solid-icon-v1")]',
                './/div[contains(@class, "map-icon")]',
                './/div[contains(@class, "location-icon")]',
                './/button[contains(@class, "map")]'
            ]
            
            for selector in selectors:
                try:
                    wait = WebDriverWait(tile, 5)
                    map_icon = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    ActionChains(self.driver).move_to_element(map_icon).click().perform()
                    print(f"Map icon clicked successfully using selector: {selector}")
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"Error clicking map icon: {e}")
            return False

    def wait_for_map_to_load(self, timeout=15):
        """
        More flexible map loading check.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            # Try different map container selectors
            selectors = [
                self.locators['map_section'],
                '//div[contains(@class, "map")]',
                '//div[contains(@class, "location-view")]'
            ]
            
            for selector in selectors:
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    print("Map section loaded successfully.")
                    return
                except:
                    continue
                    
            print("Map section not found with any selector.")
            
        except Exception as e:
            print(f"Error waiting for map section to load: {e}")