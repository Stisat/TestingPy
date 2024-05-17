import yaml
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


with open("testdata.yaml") as f:
    test_data = yaml.safe_load(f)

browser = test_data["browser"]
# service = Service(test_data["driver_path"])



class Site:

    def __init__(self, address):
        if browser == "firefox":
            service = Service(executable_path=GeckoDriverManager().install())
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(service=service, options=options)
        elif browser == "chrome":
            service = Service(executable_path=ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.get(address)

    def find_element(self, mode, path):
        if mode == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, path)
            time.sleep(test_data["sleep_time"])
        elif mode == "xpath":
            element = self.driver.find_element(By.XPATH, path)
            time.sleep(test_data["sleep_time"])
        else:
            element = None
        return element

    def get_element_property(self, mode, path, property):
        element = self.find_element(mode, path)
        return element.value_of_css_property(property)

    def go_home_page(self, address):
        self.driver.get(address)

    def close(self):
        self.driver.close()
