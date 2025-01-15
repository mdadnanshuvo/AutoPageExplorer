from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_property_info(tile, wait_time=5):
    """
    Extracts property information from a tile element, ensuring no missing values.

    Args:
        tile (WebElement): The tile element.
        wait_time (int): Maximum time to wait for elements to load.

    Returns:
        dict: A dictionary containing the property information, including the data-id.

    Raises:
        Exception: If any required element is missing.
    """
    info = {}
    wait = WebDriverWait(tile, wait_time)

    try:
        # Extract data-id directly from the tile element
        info['data_id'] = tile.get_attribute('data-id')

        # Use explicit class and ID locators
        info['title'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[@id[contains(., "details-btn-anchor")]]')
            )
        ).text

        info['rating'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[contains(@class, "review-general")]')
            )
        ).text

        info['review'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[contains(@class, "review-general")]')
            )
        ).text

        info['number_of_reviews'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[contains(@class, "number-of-review")]')
            )
        ).text

        info['price'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[contains(@class, "price-info") and contains(@class, "js-price-value")]')
            )
        ).text

        info['property_type'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/*[contains(@class, "property-type") and contains(@class, "color-dark-light")]')
            )
        ).text

    except Exception as e:
        # Log error and re-raise to ensure issues are identified
        print(f"Error extracting property info from tile (data-id: {info.get('data_id', 'unknown')}): {e}")
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
        # Mandatory fields from the map info window
        map_info['property_type'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/div[contains(@class, "info-window-amenities")]')
            )
        ).text

        map_info['title'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/a[contains(@class, "info-window-title")]')
            )
        ).text

        map_info['rating'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/span[contains(@class, "review-general")]')
            )
        ).text

        map_info['number_of_reviews'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/span[contains(@class, "number-of-reviews")]')
            )
        ).text

        map_info['price'] = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, './/span[contains(@class, "js-nearby-price-value")]')
            )
        ).text

    except Exception as e:
        # Log error and re-raise
        print(f"Error extracting map info: {e}")
        raise

    return map_info
