from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def process_hybrid_page(driver, tile, wait_time=10):
    """
    Interact with the hybrid page by clicking the title link, fetching data,
    and returning to the category page.

    Args:
        driver (WebDriver): The WebDriver instance.
        tile (WebElement): The tile element containing the title link.
        wait_time (int): Maximum time to wait for elements to load.

    Returns:
        dict: Data fetched from the hybrid page.
    """
    original_window = driver.current_window_handle

    try:
        # Locate and click the title link in the tile
        title_link = tile.find_element(By.XPATH, './/a[contains(@id, "details-btn-anchor")]')
        ActionChains(driver).move_to_element(title_link).click().perform()
        print("Clicked the title link. New tab opened.")

        # Wait for the new tab to open
        WebDriverWait(driver, wait_time).until(
            lambda drv: len(drv.window_handles) > 1
        )
        new_tab = [handle for handle in driver.window_handles if handle != original_window][0]
        driver.switch_to.window(new_tab)
        print("Switched to the new tab (Hybrid page).")

        # Extract data from the hybrid page
        hybrid_data = {}

        wait = WebDriverWait(driver, wait_time)

        # Extract property title
        hybrid_data['title'] = wait.until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "js-ai-content-property-name")]'))
        ).text

        # Extract property type
        hybrid_data['property_type'] = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "js-property-type")]'))
        ).text

        # Extract rating and reviews
        rating_review = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "rating-review")]'))
        )
        hybrid_data['rating'] = rating_review.find_element(
            By.XPATH, './/strong[contains(@class, "review-score")]'
        ).text
        hybrid_data['number_of_reviews'] = rating_review.find_element(
            By.XPATH, './/span[contains(@class, "number-of-reviews")]'
        ).text

        # Extract price
        hybrid_data['price'] = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[@id="js-price-per-night"]'))
        ).text

        print(f"Data extracted from the hybrid page: {hybrid_data}")

        # Close the hybrid page and switch back to the category page
        driver.close()
        driver.switch_to.window(original_window)
        print("Closed the hybrid page and returned to the category page.")

        return hybrid_data

    except Exception as e:
        print(f"Error interacting with the hybrid page: {e}")
        raise
