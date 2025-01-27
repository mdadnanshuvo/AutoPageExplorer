from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.utility_func import xpaths_for_hybrid


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

    Raises:
        Exception: If any required element is missing or unavailable.
    """
    paths = xpaths_for_hybrid()
    original_window = driver.current_window_handle

    try:
        # Locate and click the title link in the tile
        title_link = tile.find_element(By.XPATH, paths["property_tiles"])
        ActionChains(driver).move_to_element(title_link).click().perform()

        # Wait for the new tab to open
        WebDriverWait(driver, wait_time).until(lambda drv: len(drv.window_handles) > 1)
        new_tab = [
            handle for handle in driver.window_handles if handle != original_window
        ][0]
        driver.switch_to.window(new_tab)

        # Extract data from the hybrid page
        hybrid_data = {}
        wait = WebDriverWait(driver, wait_time)

        # Extract property title and keep only the part before '|'
        hybrid_data["title"] = (
            wait.until(
                EC.presence_of_element_located((By.XPATH, paths["property_title"]))
            )
            .text.split("|")[0]
            .strip()
        )

        # Extract property type from the availability title
        availability_title = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["property_type"]))
        ).text.strip()
        words = availability_title.split()
        if (
            len(words) >= 3
            and words[0].lower() == "check"
            and words[2].lower() == "availability"
        ):
            hybrid_data["property_type"] = words[1]
        else:
            raise Exception(
                f"Unexpected format for availability title: {
                            availability_title}"
            )

        # Extract rating and reviews dynamically
        rating_review = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["rating_review_div"]))
        )
        if rating_review.find_elements(By.XPATH, paths["star_ratings"]):
            # Case: Standard rating and reviews
            hybrid_data["rating"] = rating_review.find_element(
                By.XPATH, paths["star_ratings"]
            ).text
            hybrid_data["number_of_reviews"] = rating_review.find_element(
                By.XPATH, paths["number_of_reviews"]
            ).text
        elif rating_review.find_elements(By.XPATH, paths["review_general"]):
            # Case: New listing, no reviews
            hybrid_data["rating"] = "New"
            hybrid_data["number_of_reviews"] = rating_review.find_element(
                By.XPATH, './/span[contains(@class, "text-bold new-text")]'
            ).text
        else:
            # Raise an exception if no matching structure is found
            raise Exception(
                "Unable to extract rating and review details from the hybrid page."
            )

        # Extract price
        hybrid_data["price"] = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["price_info"]))
        ).text

        # Close the hybrid page and switch back to the category page
        driver.close()
        driver.switch_to.window(original_window)
        return hybrid_data

    except Exception as e:
        # Ensure we always return to the original window
        driver.switch_to.window(original_window)
        raise
