import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    # Replace spaces with dashes for URL compatibility
    country = faker.country().replace(" ", "-").lower()
    return f"{base_url}{country}"

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
        return total_tiles
    except Exception as e:
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
        return page_layout == "Category"
    except Exception as e:
        print(f"Error while checking ScriptData.pageLayout: {e}")
        return False

def extract_property_info(tile, wait_time=1.5):
    """
    Extracts property information and the data-id from a tile element.

    Args:
        tile (WebElement): The tile element.
        wait_time (float): Maximum time to wait for elements to load.

    Returns:
        tuple: A tuple containing:
            - dict: A dictionary with the property information from the tile.
            - str: The property_id extracted from the data-id attribute.

    Raises:
        Exception: If any required element is missing.
    """
    paths = xpaths_for_category()  # Function must return a dictionary of XPath mappings
    info = {}
    wait = WebDriverWait(tile, wait_time)

    try:
        # Extract property ID (data-id attribute)
        property_id = tile.get_attribute("data-id")
        if not property_id:
            raise Exception("data-id attribute not found in tile element.")

        # Extract property type
        info["property_type"] = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["property_type"]))
        ).text

        # Extract property title
        info["title"] = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["property_title"]))
        ).text

        # Extract rating and reviews
        rating_review_div = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["rating_review_div"]))
        )

        # Handle dynamic rating and review structures
        if rating_review_div.find_elements(By.XPATH, paths["review_general"]):
            info["rating"] = rating_review_div.find_element(
                By.XPATH, paths["review_general"]
            ).text
            info["number_of_reviews"] = rating_review_div.find_element(
                By.XPATH, paths["number_of_reviews"]
            ).text

        elif rating_review_div.find_elements(By.XPATH, paths["star_ratings"]):
            star_rating = rating_review_div.find_element(
                By.XPATH, paths["star_ratings"]
            ).get_attribute("class")
            info["rating"] = star_rating.split("star-icons-")[-1]
            info["number_of_reviews"] = rating_review_div.find_element(
                By.XPATH, paths["number_of_reviews"]
            ).text

        elif rating_review_div.find_elements(By.XPATH, paths["number_of_reviews"]):
            info["rating"] = "New"
            info["number_of_reviews"] = rating_review_div.find_element(
                By.XPATH, paths["number_of_reviews"]
            ).text

        else:
            info["rating"] = "N/A"
            info["number_of_reviews"] = "N/A"

        # Extract price
        price_text = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["price_info"]))
        ).text
        info["price"] = price_text.split(" ", 1)[1] if " " in price_text else price_text

    except Exception as e:
        print(f"Error extracting property info from tile: {e}")
        raise
    return info, property_id

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
    paths = xpaths_for_category()
    map_info = {}
    wait = WebDriverWait(driver, wait_time)

    try:
        # Extract property type
        map_info["property_type"] = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["map_property_type"]))
        ).text

        # Extract property title
        map_info["title"] = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["map_property_title"]))
        ).text

        # Extract rating and reviews dynamically
        review_ratings_div = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["map_review_ratings_div"]))
        )

        # Handle different structures of rating and reviews
        if review_ratings_div.find_elements(By.XPATH, paths["map_review_general"]):
            # Case: Standard rating and reviews
            map_info["rating"] = review_ratings_div.find_element(
                By.XPATH, paths["map_review_general"]
            ).text
            map_info["number_of_reviews"] = review_ratings_div.find_element(
                By.XPATH, paths["map_num_of_reviews"]
            ).text
        elif review_ratings_div.find_elements(By.XPATH, paths["map_new_reviews"]):
            # Case: New listing, no reviews
            map_info["rating"] = "New"
            map_info["number_of_reviews"] = review_ratings_div.find_element(
                By.XPATH, paths["map_new_reviews"]
            ).text
        else:
            # Raise an exception if no matching structure is found
            raise Exception(
                "Unable to extract rating and review details from the map section."
            )

        # Extract price
        map_info["price"] = wait.until(
            EC.presence_of_element_located((By.XPATH, paths["map_price"]))
        ).text

    except Exception as e:
        print(f"Error extracting map info: {e}")
        raise

    return map_info


def generate_comparison_report(
    ID,
    tile_data,
    map_data,
    hybrid_data,
    url,
    domain="www.varoom.com",
    page="Category",
    test_case="Test for data consistency",
):
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
        "ID": ID,
        "tile_info": tile_data,
        "map_info_window": map_data,
        "details_info": hybrid_data,
    }

    # Create report data
    report_data = [
        {
            "Key": domain,  # Assuming "_id" is in tile_data
            "URL": url,
            "Page": page,
            "Test Case": test_case,
            "Passed": passed,
            # Convert dictionary to string for readability
            "Comments": str(comments),
        }
    ]

    # Load existing report or create new
    try:
        existing_df = pd.read_excel(output_file)
        df = pd.concat([existing_df, pd.DataFrame(report_data)], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(report_data)

    # Save updated report
    df.to_excel(output_file, index=False)


def xpaths_for_category():
    """
    This function will return all the Xpaths responsible for category page.
    """
    xpaths_file = "data/xpaths.xlsx"
    # Make sure the 'base_url' is set as index
    xpaths_df = pd.read_excel(xpaths_file, index_col=0)

    page_type = "Category"
    page_xpaths = xpaths_df.loc[xpaths_df["page_type"] == page_type].iloc[0]

    return page_xpaths


def xpaths_for_hybrid():
    # Load the Excel file
    xpaths_file = "data/xpaths.xlsx"  # Path to your Excel file
    xpaths_df = pd.read_excel(xpaths_file)

    # Filter rows for page_type = 'Hybrid'
    page_type = "Hybrid"
    hybrid_xpaths = xpaths_df[xpaths_df["page_type"] == page_type]

    if not hybrid_xpaths.empty:
        # Convert the row to a dictionary and return
        return hybrid_xpaths.iloc[0].to_dict()
    else:
        return "No xpaths found for Hybrid page type."
