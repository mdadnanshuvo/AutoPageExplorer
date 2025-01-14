from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_property_info(tile, wait_time=20):
    """
    Extracts property information from a tile element, ensuring no missing values.

    Args:
        tile (WebElement): The tile element.
        wait_time (int): Maximum time to wait for elements to load.

    Returns:
        dict: A dictionary containing the property information.

    Raises:
        Exception: If any required element is missing.
    """
    info = {}
    wait = WebDriverWait(tile, wait_time)

    # Mandatory fields
    info['title'] = wait.until(
        EC.presence_of_element_located((By.XPATH, './/a[@id[contains(., "details-btn-anchor")]]'))
    ).text

    info['rating'] = wait.until(
        EC.presence_of_element_located((By.XPATH, './/span[@class="review-general"]'))
    ).text

    info['review'] = wait.until(
        EC.presence_of_element_located((By.XPATH, './/span[@class="review-general"]'))
    ).text

    info['number_of_reviews'] = wait.until(
        EC.presence_of_element_located((By.XPATH, './/span[@class="number-of-review"]'))
    ).text

    info['price'] = wait.until(
        EC.presence_of_element_located((By.XPATH, './/span[@class="price-info js-price-value"]'))
    ).text

    info['property_type'] = wait.until(
        EC.presence_of_element_located((By.XPATH, './/span[@class="property-type color-dark-light font-11 ellipsis"]'))
    ).text

    return info
