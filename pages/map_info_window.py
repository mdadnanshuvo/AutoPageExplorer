from .base_page import BasePage
from selenium.webdriver.common.by import By


class MapInfoWindow(BasePage):
    """
    Represents the Map Info Window and provides methods to extract property information.
    """

    def __init__(self, driver):
        """
        Initializes the MapInfoWindow instance with the WebDriver.
        
        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.locators = {
            'map_info_window': '//div[contains(@class, "map-info-window")]'
        }

    def is_displayed(self):
        """
        Checks if the Map Info Window is displayed.
        
        Returns:
            bool: True if the Map Info Window is visible, False otherwise.
        """
        try:
            map_info_element = self.wait_for_element((By.XPATH, self.locators['map_info_window']))
            return map_info_element.is_displayed()
        except Exception as e:
            print(f"Error checking Map Info Window visibility: {e}")
            return False

    def get_info(self):
        """
        Extracts information from the Map Info Window.
        
        Returns:
            dict: A dictionary containing the property information from the Map Info Window.
        """
        if not self.is_displayed():
            raise Exception("Map Info Window is not visible or could not be located.")
        
        return ""
