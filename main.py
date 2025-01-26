# main.py

from utils.driver_utils import setup_driver
from pages.category_page import CategoryPage
import time
import random


def generate_scroll_sequence(total_tiles, num_scrolls=10):
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

        random_tiles = category_page.process_tiles_randomly_one_by_one(
            all_tiles, valid_url)
        # Process tiles one by one
        print("\n=== Phase 3: Processing Individual Tiles ===")
        results = []
        for tile in random_tiles:
            try:
                # Try to interact with map first
                if category_page.click_map_icon(tile):
                    pass

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
            except Exception as e:
                pass

    print("\n=== Processing Complete ===")


if __name__ == "__main__":
    main()
