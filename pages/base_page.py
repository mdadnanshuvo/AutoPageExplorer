from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        """
        Waits for an element to be present on the page.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def get_element_text(self, locator):
        """
        Gets the text of a web element.
        """
        element = self.wait_for_element(locator)
        return element.text

    def click_element(self, locator):
        """
        Clicks a web element.
        """
        element = self.wait_for_element(locator)
        element.click()

    def find_elements(self, locator):
        """
        Finds all elements matching the locator.
        """
        return self.driver.find_elements(*locator)

    def navigate_to(self, url):
        """
        Navigates to a specified URL.
        """
        self.driver.get(url)

    def get_title(self):
        """
        Gets the title of the current page.
        """
        return self.driver.title

    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        """
        Waits for an element to be clickable.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of the page.
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time if necessary

    def scroll_to_top(self):
        """
        Scrolls to the top of the page.
        """
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)  # Adjust the sleep time if necessary

    def scroll_from_top_to_bottom_and_back(self):
        """
        Scrolls from the top to the bottom of the page and then back to the top.
        """
        self.scroll_to_bottom()
        self.scroll_to_top()
