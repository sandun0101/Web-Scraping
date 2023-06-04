from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Use the appropriate WebDriver for your browser
        self.wait = WebDriverWait(self.driver, 10)

    def get_page_content(self, url):
        self.driver.get(url)

    def wait_for_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, element):
        element.click()

    def find_element_text(self, element):
        return element.text.strip()

    def close_browser(self):
        print('Scrape Completed...')
        self.driver.quit()

    def handle_exception(self):
        # Handle any exceptions that may occur during scraping
        pass
