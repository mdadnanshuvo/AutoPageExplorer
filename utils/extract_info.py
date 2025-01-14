from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_property_info(tile, wait_time=10):
    """
    Extracts property information from a tile element.

    Args:
        tile (WebElement): The tile element.
        wait_time (int): Maximum time to wait for elements to load.

    Returns:
        dict: A dictionary containing the property information.
    """
    info = {}
    try:
        wait = WebDriverWait(tile, wait_time)
        info['title'] = wait.until(EC.presence_of_element_located((By.XPATH, './/a[@id[contains(., "details-btn-anchor")]]'))).text
        info['rating'] = wait.until(EC.presence_of_element_located((By.XPATH, './/span[@class="review-general"]'))).text
        info['review'] = tile.find_element(By.XPATH, './/span[@class="review-general"]').text
        info['number_of_reviews'] = tile.find_element(By.XPATH, './/span[@class="number-of-review"]').text
        info['price'] = tile.find_element(By.XPATH, './/span[@class="price-info js-price-value"]').text
        info['property_type'] = tile.find_element(By.XPATH, './/span[@class="property-type color-dark-light font-11 ellipsis"]').text
    except Exception as e:
        print(f"Error extracting property info: {e}")
    return info
