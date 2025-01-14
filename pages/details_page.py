# pages/details_page.py
from .base_page import BasePage
from utils.excel_utils import get_locators
from selenium.webdriver.common.by import By

class DetailsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = get_locators("config/locators.xlsx")

    def get_info(self):
        title = self.get_element_text((By.XPATH, self.locators['details_title']))
        price = self.get_element_text((By.XPATH, self.locators['details_price']))
        rating = self.get_element_text((By.XPATH, self.locators['details_rating']))
        review = self.get_element_text((By.XPATH, self.locators['details_review']))
        return {'title': title, 'price': price, 'rating': rating, 'review': review}