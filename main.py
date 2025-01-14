from selenium import webdriver
from pages.category_page import CategoryPage

def main():
    """
    Main function to validate map icon interaction for random tiles.
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    try:
        category_page = CategoryPage(driver)
        valid_url = category_page.navigate_to_valid_category_page()
        print(f"Testing with URL: {valid_url}")

        total_tiles = category_page.get_total_tiles()
        if total_tiles == 0:
            print("No tiles found on the page. Exiting.")
            return

        all_tiles = category_page.get_all_property_tiles(total_tiles)
        random_tiles = category_page.get_random_property_tiles(all_tiles)
        print(f"Selected {len(random_tiles)} random property tiles.")

        for i, tile in enumerate(random_tiles):
            try:
                data = category_page.process_tile(tile)
                print(f"Tile {i + 1}: {data}")
            except Exception as e:
                print(f"Failed to process tile {i + 1}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
