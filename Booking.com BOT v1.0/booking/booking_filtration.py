import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration:
    def __init__(self, driver=WebDriver):
        self.driver = driver

    def apply_star_rating(self, star_value):
        star_rating_element = self.driver.find_element(
            By.ID, "filter_group_class_:R14q:")

        star_child_elements = star_rating_element.find_elements(By.CSS_SELECTOR, '*')

        for star_element in star_child_elements:
            if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                star_element.click()

    def sort_lowest_price_first(self):
        sorters_dropdown_element = self.driver.find_element(
            By.CSS_SELECTOR,
            "button.fc63351294.a822bdf511.e2b4ffd73d.fa565176a8.f7db01295e.c334e6f658.f95c50be27.a9a04704ee")

        sorters_dropdown_element.click()

        option = self.driver.find_element(By.CSS_SELECTOR, "button[data-id='price']")
        option.click()






