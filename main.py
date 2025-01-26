# main.py

from utils.driver_utils import setup_driver
from pages.category_page import CategoryPage
import time
import random


def main():
    """
    Main function to execute the property tile processing workflow.
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

        # Smoothly scroll to the bottom of the page
        print("\n=== Scrolling the Category Page ===")
        category_page.scroll_smoothly_to_bottom(pause_time=0.5)
        print("Page scrolling completed")

        # Get total tiles after scrolling
        total_tiles = category_page.get_total_tiles()
        print(f"Total tiles after scrolling: {total_tiles}")

        # Load all tiles
        all_tiles = category_page.load_all_property_tiles(total_tiles)
        print(f"Loaded {len(all_tiles)} tiles")

        random_tiles = random.sample(all_tiles, 10)

        # Process tiles one by one
        print("\n=== Processing Individual Tiles ===")
        results = []
        for tile in random_tiles:
            try:
                # Process the tile
                result = category_page.process_tile(tile, valid_url)
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

    finally:
        if driver:
            try:
                # Close all tabs/windows
                driver.quit()
                print("\nAll browser windows closed successfully")
            except Exception:
                pass

    print("\n=== Processing Complete ===")


if __name__ == "__main__":
    main()
