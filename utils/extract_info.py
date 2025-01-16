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

        # Extract rating and reviews using the rating-review class
        rating_review_div = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/div[contains(@class, "rating-review")]')
            )
        )

        # Extract rating
        info['rating'] = rating_review_div.find_element(
            By.XPATH, './/span[contains(@class, "review-general")]'
        ).text

        # Extract number of reviews
        info['number_of_reviews'] = rating_review_div.find_element(
            By.XPATH, './/span[contains(@class, "number-of-review")]'
        ).text

        # Extract price
        info['price'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[contains(@class, "price-info") and contains(@class, "js-price-value")]')
            )
        ).text

    except Exception as e:
        print(f"Error extracting property info from tile: {e}")
        raise

    return info


def extract_map_info(driver, wait_time=5):
    """
    Extracts property information from the map section of the page.

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

        # Extract rating and reviews using info-window-review-ratings class
        review_ratings_div = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/div[contains(@class, "info-window-review-ratings")]')
            )
        )

        # Extract rating
        map_info['rating'] = review_ratings_div.find_element(
            By.XPATH, './/span[contains(@class, "review-general")]'
        ).text

        # Extract number of reviews
        map_info['number_of_reviews'] = review_ratings_div.find_element(
            By.XPATH, './/span[contains(@class, "number-of-reviews")]'
        ).text

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
