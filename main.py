from selenium import webdriver
from pages.category_page import CategoryPage
import time

def main():
    """
    Main function to fetch property data from random tiles, processing one at a time.
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    try:
        category_page = CategoryPage(driver)
        valid_url = category_page.navigate_to_valid_category_page()
        print(f"Testing with URL: {valid_url}")

        # Fetch total number of tiles
        total_tiles = category_page.get_total_tiles()
        if total_tiles == 0:
            print("No tiles found on the page. Exiting.")
            return

        # Fetch random tiles and process them one by one
        random_tiles = category_page.get_random_property_tiles()
        print(f"Selected {len(random_tiles)} random property tiles.")

        for i, tile in enumerate(random_tiles):
            retries = 3  # Retry threshold for each tile
            success = False

            while retries > 0 and not success:
                data = category_page.process_tile(tile)
                if data:
                    print(f"Tile {i + 1}: {data}")
                    success = True
                else:
                    retries -= 1
                    print(f"Retrying tile {i + 1}... ({3 - retries} retries left)")

            if not success:
                print(f"Failed to process tile {i + 1} after multiple attempts. Skipping.")
            else:
                # Add a delay before moving to the next tile
                time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
