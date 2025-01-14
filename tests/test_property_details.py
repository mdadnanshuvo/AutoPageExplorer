import unittest
from selenium import webdriver
from pages.category_page import CategoryPage
from utils.url_helper import get_random_category_url  # Import the URL generator

class TestCategoryPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the WebDriver and base URL for all tests in this class.
        """
        cls.driver = webdriver.Chrome()  # Ensure the correct WebDriver is installed
        cls.driver.implicitly_wait(10)  # Set implicit wait time for element loading
        cls.base_url = get_random_category_url()  # Generate a random category URL

    @classmethod
    def tearDownClass(cls):
        """
        Quit the WebDriver after all tests in this class have run.
        """
        if cls.driver:
            cls.driver.quit()

    def setUp(self):
        """
        Set up for each individual test.
        """
        self.assertIsNotNone(self.driver, "WebDriver is not set!")
        self.assertIsNotNone(self.base_url, "Base URL is not set!")
        self.category_page = CategoryPage(self.driver)
        self.category_page.navigate_to(self.base_url)

    def test_category_page_loads(self):
        """
        Test to ensure the Category Page loads and property tiles are present.
        """
        print(f"Testing with URL: {self.base_url}")  # Debugging output

        # Verify if property tiles are present
        property_tiles = self.category_page.get_property_tiles()
        self.assertGreater(len(property_tiles), 0, "No property tiles found!")
        print(f"Found {len(property_tiles)} property tiles.")  # Debugging output


if __name__ == "__main__":
    unittest.main()
