# utils/driver_utils.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_driver():
    """
    Set up and configure the Chrome WebDriver with optimal settings.
    
    Returns:
        webdriver: Configured Chrome WebDriver instance
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start with maximized window
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver
