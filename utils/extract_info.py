import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
