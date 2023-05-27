import os
from selenium import webdriver
from utils.constant import BASE_URL
from selenium.webdriver.common.by import By
from utils.review_report import ReviewReport


class TaskRabbit(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\chrome_driver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(TaskRabbit, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(BASE_URL)

    def report_result(self):
        author = self.find_elements(By.CSS_SELECTOR, 'div.sc-jRwbcX.bLnjzR')
        return author






