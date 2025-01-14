import unittest
from selenium import webdriver
from config.config import Config

class TestRandomCategoryPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.base_url = Config.get_random_country_url()
        cls.driver.get(cls.base_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_page_loads(self):
        # Check that the page title contains some expected text (like "RentByOwner" or similar)
        self.assertIn("RentByOwner", self.driver.title)

if __name__ == "__main__":
    unittest.main()