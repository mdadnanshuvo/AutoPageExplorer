from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.category_page import CategoryPage
import time
import sys
import random


def setup_driver():
    """
    Set up and configure the Chrome WebDriver with optimal settings.
    
    Returns:
        webdriver: Configured Chrome WebDriver instance
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start with maximized window
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def generate_scroll_sequence(total_tiles, num_scrolls=20):
    """
    Generate a sequence of tile indices to scroll to.
    
    Args:
        total_tiles (int): Total number of tiles available
        num_scrolls (int): Number of scrolls to perform
    
    Returns:
        list: List of tile indices to scroll to
    """
    if total_tiles <= num_scrolls:
        return list(range(total_tiles))
    
    # Generate evenly spaced indices with some randomization
    base_interval = total_tiles // num_scrolls
    indices = []
    
    for i in range(num_scrolls):
        base_index = i * base_interval
        # Add some randomization within the interval
        random_offset = random.randint(-base_interval//4, base_interval//4)
        index = max(0, min(total_tiles - 1, base_index + random_offset))
        indices.append(index)
    
    # Ensure indices are unique and sorted
    return sorted(list(set(indices)))


def main():
    """
    Main function to execute the property tile processing workflow with initial scrolling
    """
    driver = None
    start_time = time.time()
    
    try:
        print("\n=== Starting Property Tile Processing ===")
        
        # Initialize driver with optimal settings
        driver = setup_driver()
        print("Browser initialized successfully")
        
        # Initialize category page and navigate to valid URL
        category_page = CategoryPage(driver)
        valid_url = category_page.navigate_to_valid_category_page()
        print(f"\nNavigated to valid category page: {valid_url}")
        
        # Get initial tile count
        total_tiles = category_page.get_total_tiles()
        print(f"Initial tile count: {total_tiles}")
        
        # Load all tiles
        print("\n=== Phase 1: Loading All Tiles ===")
        all_tiles = category_page.load_all_property_tiles(total_tiles)
        print(f"Loaded {len(all_tiles)} tiles")
        
        # Generate scroll sequence and perform initial scrolling
        print("\n=== Phase 2: Performing Initial Page Scrolling ===")
        scroll_indices = generate_scroll_sequence(len(all_tiles))
        print(f"Generated {len(scroll_indices)} scroll points")
        
        scrolled_tiles = category_page.scroll_to_specific_tiles(
            all_tiles,
            scroll_indices,
            smooth=True
        )
        print(f"Successfully scrolled through {len(scrolled_tiles)} tiles")
        
        random_tiles = category_page.process_tiles_randomly_one_by_one(all_tiles)
        # Process tiles one by one
        print("\n=== Phase 3: Processing Individual Tiles ===")
        results = []
        for tile in random_tiles:
            try:
                # Try to interact with map first
                if category_page.click_map_icon(tile):
                    category_page.wait_for_map_to_load()
                
                # Process the tile
                result = category_page.process_tile(tile)
                results.append(result)
                print("Successfully processed tile")
                
            except Exception as e:
                print(f"Error processing tile: {e}")
        
        # Print processing summary
        print("\n=== Processing Summary ===")
        print(f"Total tiles processed: {len(results)}")
        print(f"Total time taken: {time.time() - start_time:.2f} seconds")
        
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        
    except Exception as e:
        print(f"\nCritical error occurred: {str(e)}")
        import traceback
        print("\nFull error traceback:")
        traceback.print_exc()
        
    finally:
        if driver:
            try:
                driver.quit()
                print("\nBrowser closed successfully")
            except Exception as e:
                print(f"\nError closing browser: {str(e)}")
        
        print("\n=== Processing Complete ===")


if __name__ == "__main__":
    main()