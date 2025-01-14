from utils.url_helper import get_random_country_url

class Config:
    BASE_URL_TEMPLATE = "https://www.rentbyowner.com/all/{country}"
    LOCATORS_FILE = "config/locators.xlsx"
    TEST_DATA_FILE = "data/test_data.xlsx"

    @staticmethod
    def get_random_country_url():
        return get_random_country_url(Config.BASE_URL_TEMPLATE)