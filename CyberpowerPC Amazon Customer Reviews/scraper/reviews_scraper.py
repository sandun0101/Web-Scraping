import os
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import scraper.constants as const
from utils.data_processing import list_to_csv


class ReviewsScraper(webdriver.Chrome):
    """
       A web scraper for extracting reviews using Selenium and Chrome WebDriver.

       Args:
           driver_path (str): Path to the Chrome WebDriver executable.
               Default: "C:\web_drivers\chromedriver"
           teardown (bool): Whether to close the WebDriver when the scraper is done.
               Default: False
       """
    def __init__(self, driver_path=r"C:\web_drivers\chromedriver", teardown=False):
        """
           Initialize the ReviewsScraper object.

           Args:
               driver_path (str): Path to the Chrome WebDriver executable.
                   Default: "C:\web_drivers\chromedriver"
               teardown (bool): Whether to close the WebDriver when the scraper is done.
                   Default: False
        """
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        super(ReviewsScraper, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context and perform necessary cleanup.
        """
        if self.teardown:
            self.quit()

    def land_first_page(self):
        """
           Navigate to the first page of the website.
        """
        self.get(const.BASE_URL)

    def login(self):
        """
            Perform login using the provided email and password.

            Args:
                email (str): User's email address.
                password (str): User's password.
        """
        email = input("Enter your amazon email: ")
        email_field = self.find_element(By.ID, "ap_email")
        email_field.clear()
        email_field.send_keys(email)

        continue_button = self.find_element(By.ID, "continue")
        continue_button.click()
        time.sleep(1)

        password = input("Enter your password: ")
        password_field = self.find_element(By.ID, "ap_password")
        password_field.clear()
        password_field.send_keys(password)

        sign_in_button = self.find_element(By.ID, "signInSubmit")
        sign_in_button.click()

        # not_now_button = self.find_element(By.ID, "ap-account-fixup-phone-skip-link")
        # not_now_button.click()

    def review_scraper(self):
        """
            Scrape reviews from multiple pages on Amazon.

            This method navigates through multiple pages of reviews on Amazon for a specific product and extracts the name,
            star rating, and review text for each review. It stores the extracted data in a list of lists.

            Returns:
                list: A list of lists containing the extracted review data. Each inner list contains the name, star rating,
                    and review text for a single review.
        """

        reviews_data = []

        total_pages = 100
        progress_bar = tqdm(total=total_pages, desc="Scraping Reviews")

        for i in range(1, total_pages + 1):
            self.get(f'https://www.amazon.com/CyberpowerPC-Xtreme-i7-12700F-GeForce-GXiVR8040A12/product-reviews'
                     f'/B0B7872PZR/ref=cm_cr_arp_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber={i}')

            time.sleep(1)
            review_boxes = self.find_elements(By.CSS_SELECTOR, 'div[data-hook="review"]')

            for review_box in review_boxes:
                name_element = review_box.find_element(
                    By.CSS_SELECTOR, 'span[class="a-profile-name"]').text.strip()

                star_rating_element = review_box.find_element(
                    By.CSS_SELECTOR, 'i[data-hook="review-star-rating"]')
                star_rating_text = star_rating_element.get_attribute('innerHTML')

                star_rating_text = BeautifulSoup(star_rating_text, 'html.parser').get_text().strip()

                review_element = review_box.find_element(
                    By.CSS_SELECTOR, 'span[data-hook="review-body"]').text.strip()

                reviews_data.append([name_element, star_rating_text, review_element])

            progress_bar.update(1)

        progress_bar.close()

        list_to_csv(reviews_data)




