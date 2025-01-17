import os
import pandas as pd
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from faker import Faker

def get_random_category_url(base_url="https://www.varoom.com/all/"):
    """
    Generates a random category URL by appending a random country to the base URL.

    Args:
        base_url (str): The base URL for the category page.

    Returns:
        str: A complete category page URL with a random country.
    """
    faker = Faker()
    country = faker.country().replace(" ", "-").lower()  # Replace spaces with dashes for URL compatibility
    return f"{base_url}{country}"


def scroll_and_load(driver, tiles_xpath, total_tiles, container=None, center_tiles=False, initial_scroll_time=0.1):
    """
    Dynamically scrolls and loads elements matching the provided XPath within a specific container,
    with an optional initial scrolling time and tile centralization.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        tiles_xpath (str): XPath to locate tile elements.
        total_tiles (int): Total number of tiles expected.
        container (WebElement): Optional container element to scope the search.
        center_tiles (bool): Scroll each tile to the center of the viewport if True.
        initial_scroll_time (int): Time in seconds for initial dynamic scrolling.

    Returns:
        list: List of WebElements found.
    """
    # Perform initial scrolling to allow the page to load dynamically
    start_time = time.time()
    while time.time() - start_time < initial_scroll_time:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        

    print("Initial scrolling completed. Starting tile loading...")

    # Scroll and load tiles
    loaded_tiles = []
    scroll_attempts = 0
    max_scroll_attempts = 20  # Adjust as necessary

    # Use container if provided, otherwise scroll the document body
    scroll_target = container if container else driver.find_element(By.TAG_NAME, "body")

    while len(loaded_tiles) < total_tiles and scroll_attempts < max_scroll_attempts:
        loaded_tiles = driver.find_elements(By.XPATH, tiles_xpath)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_target)
        time.sleep(0.5)  # Allow time for loading
        scroll_attempts += 1

    print(f"Loaded {len(loaded_tiles)} tiles after scrolling.")

    # Optionally center each tile in the viewport
    if center_tiles:
        for tile in loaded_tiles:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", tile)
                time.sleep(0.5)  # Allow smooth scrolling
                print("Tile centered.")
            except Exception as e:
                print(f"Error centering tile: {e}")

    return loaded_tiles


def select_random_elements(elements, count=10):
    """
    Selects a random subset of elements from a given list.

    Args:
        elements (list): List of elements to choose from.
        count (int): Number of random elements to select.

    Returns:
        list: Randomly selected elements.
    """
    if len(elements) <= count:
        return elements
    return random.sample(elements, count)



def get_total_tiles_count(driver):
    """
    Retrieve the total number of tiles using ScriptData.pageData.Items.length.

    Args:
        driver (WebDriver): Selenium WebDriver instance.

    Returns:
        int: Total number of tiles on the page.
    """
    try:
        total_tiles = driver.execute_script("return ScriptData.pageData.Items.length;")
        print(f"Total tiles found: {total_tiles}")
        return total_tiles
    except Exception as e:
        print(f"Error fetching total tiles count: {e}")
        return 0


def is_category_page(driver):
    """
    Checks if the current page is a Category Page using the ScriptData.pageLayout variable.

    Args:
        driver (WebDriver): Selenium WebDriver instance.

    Returns:
        bool: True if the page is a Category Page, False otherwise.
    """
    try:
        # Execute JavaScript to get the value of ScriptData.pageLayout
        page_layout = driver.execute_script("return ScriptData.pageLayout;")
        print(f"ScriptData.pageLayout: {page_layout}")  # Debugging output
        return page_layout == "Category"
    except Exception as e:
        print(f"Error while checking ScriptData.pageLayout: {e}")
        return False



def extract_property_info(tile, wait_time=0.5):
    """
    Extracts property information from a tile element.

    Args:
        tile (WebElement): The tile element.
        wait_time (float): Maximum time to wait for elements to load.

    Returns:
        dict: A dictionary containing the property information from the tile.

    Raises:
        Exception: If any required element is missing.
    """
    info = {}
    wait = WebDriverWait(tile, wait_time)

    try:
        # Extract property type
        info['property_type'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[contains(@class, "property-type") and contains(@class, "color-dark-light")]')
            )
        ).text

        # Extract property title
        info['title'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[@id[contains(., "details-btn-anchor")]]')
            )
        ).text

        # Extract rating and reviews
        rating_review_div = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/div[contains(@class, "rating-review")]')
            )
        )

        # Handle dynamic rating and review structures
        if rating_review_div.find_elements(By.XPATH, './/span[contains(@class, "review-general")]'):
            # Case 1: Standard rating and reviews
            info['rating'] = rating_review_div.find_element(By.XPATH, './/span[contains(@class, "review-general")]').text
            info['number_of_reviews'] = rating_review_div.find_element(By.XPATH, './/span[contains(@class, "number-of-review")]').text

        elif rating_review_div.find_elements(By.XPATH, './/div[contains(@class, "ratings")]'):
            # Case 2: Star-based ratings with a divider
            star_rating = rating_review_div.find_element(By.XPATH, './/div[contains(@class, "ratings")]').get_attribute('class')
            info['rating'] = star_rating.split('star-icons-')[-1]  # Extract the number of stars
            info['number_of_reviews'] = rating_review_div.find_element(By.XPATH, './/span[contains(@class, "number-of-review")]').text

        elif rating_review_div.find_elements(By.XPATH, './/span[contains(@class, "number-of-review")]'):
            # Case 3: New or no rating, only reviews
            info['rating'] = "New"
            info['number_of_reviews'] = rating_review_div.find_element(By.XPATH, './/span[contains(@class, "number-of-review")]').text

        else:
            raise Exception("Unable to extract rating and review details.")

        
        # Extract price
        price_text = wait.until(EC.presence_of_element_located((By.XPATH, './/*[contains(@class, "price-info") and contains(@class, "js-price-value")]'))).text
        price = price_text.split(' ', 1)[1]  # This removes the first word and keeps the rest

        # Store the price
        info['price'] = price




    except Exception as e:
        print(f"Error extracting property info from tile: {e}")
        raise

    return info


def extract_map_info(driver, wait_time=5):
    """
    Extracts property information from the map section of the page dynamically.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait_time (int): Maximum time to wait for elements to load.

    Returns:
        dict: A dictionary containing the property information from the map section.

    Raises:
        Exception: If any required element is missing.
    """
    map_info = {}
    wait = WebDriverWait(driver, wait_time)

    try:
        # Extract property type
        map_info['property_type'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/div[contains(@class, "info-window-amenities")]')
            )
        ).text

        # Extract property title
        map_info['title'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/a[contains(@class, "info-window-title")]')
            )
        ).text

        # Extract rating and reviews dynamically
        review_ratings_div = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/div[contains(@class, "info-window-review-ratings")]')
            )
        )

        # Handle different structures of rating and reviews
        if review_ratings_div.find_elements(By.XPATH, './/span[contains(@class, "review-general")]'):
            # Case: Standard rating and reviews
            map_info['rating'] = review_ratings_div.find_element(
                By.XPATH, './/span[contains(@class, "review-general")]'
            ).text
            map_info['number_of_reviews'] = review_ratings_div.find_element(
                By.XPATH, './/span[contains(@class, "number-of-reviews")]'
            ).text
        elif review_ratings_div.find_elements(By.XPATH, './/span[contains(@class, "number-of-review") and contains(text(), "New")]'):
            # Case: New listing, no reviews
            map_info['rating'] = "New"
            map_info['number_of_reviews'] = review_ratings_div.find_element(
                By.XPATH, './/span[contains(@class, "number-of-review") and contains(text(), "New")]'
            ).text
        else:
            # Raise an exception if no matching structure is found
            raise Exception("Unable to extract rating and review details from the map section.")

        # Extract price
        map_info['price'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/span[contains(@class, "js-nearby-price-value")]')
            )
        ).text

    except Exception as e:
        print(f"Error extracting map info: {e}")
        raise

    return map_info


def generate_comparison_report( tile_data, map_data, hybrid_data, url, domain = "www.varoom.com",page = "Category", test_case = "Test for data consistency"):
    """
    Generates an Excel report verifying the consistency of property details.

    Args:
        domain (str): Domain name (e.g., "https://www.varoom.com/").
        url (str): Category page URL.
        page (str): Page name (e.g., "Category").
        test_case (str): Test case description.
        tile_data (dict): Data from the property tile.
        map_data (dict): Data from the map info window.
        hybrid_data (dict): Data from the details page.

    Returns:
        None. Saves an Excel report in the `data` folder with `test_reports.xlsx` as the file name.
    """
    # Ensure the 'data' directory exists
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # File path for the report
    output_file = os.path.join(output_dir, "test_reports.xlsx")

    # Check consistency
    passed = tile_data == map_data == hybrid_data

    # Format comments with detailed comparison
    comments = {
        "tile_info": tile_data,
        "map_info_window": map_data,
        "details_info": hybrid_data,
    }

    # Create report data
    report_data = [{
        "Key": domain,  # Assuming "_id" is in tile_data
        "URL": url,
        "Page": page,
        "Test Case": test_case,
        "Passed": passed,
        "Comments": str(comments)  # Convert dictionary to string for readability
    }]

    # Load existing report or create new
    try:
        existing_df = pd.read_excel(output_file)
        df = pd.concat([existing_df, pd.DataFrame(report_data)], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(report_data)

    # Save updated report
    df.to_excel(output_file, index=False)
    print(f"Comparison report updated in {output_file}")
