from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.category_page import CategoryPage
import time
import sys


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


def main():
    """
    Main function to execute the property tile processing workflow:
    1. Load all tiles by scrolling
    2. Select and process random tiles one by one
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
        
        # Get total tiles count
        total_tiles = category_page.get_total_tiles()
        if total_tiles == 0:
            print("Error: No tiles found on the page")
            return
        print(f"\nDetected {total_tiles} total tiles on the page")
        
        # Phase 1: Load all properties by scrolling
        print("\n=== Phase 1: Loading All Properties ===")
        all_tiles = category_page.load_all_property_tiles(total_tiles)
        if not all_tiles:
            print("Error: Failed to load property tiles")
            return
        print(f"Successfully loaded {len(all_tiles)} property tiles")
        
        # Phase 2: Process random tiles one by one
        print("\n=== Phase 2: Processing Random Tiles ===")
        results = category_page.process_tiles_randomly_one_by_one(all_tiles, count=10)
        
        # Print summary
        print("\n=== Processing Summary ===")
        print(f"Total tiles processed: {len(results)}")
        print(f"Total time taken: {time.time() - start_time:.2f} seconds")
        
        # Print individual results
        print("\n=== Detailed Results ===")
        for i, result in enumerate(results, 1):
            print(f"\nTile {i}:")
            print(f"Index: {result['index']}")
            print("Data:", result['data'])
            
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