# this file going to include methods that parse each element details
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ReviewReport():
    def __init__(self, boxes_section_element):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_review_boxes()

    def pull_review_boxes(self):
        return self.boxes_section_element[0].find_elements(
            By.CSS_SELECTOR, 'div.sc-kImNAt.fMjDVx')

    def pull_author_name(self):

        for review_box in self.deal_boxes:
            author_name = review_box.find_element(
                By.CSS_SELECTOR, 'div.sc-jRwbcX.bLnjzR'
            ).get_attribute('outerText').strip()

            print(len(author_name))
