import os
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from utils.data_processing import save_to_excel, save_to_csv


class Reviews(webdriver.Chrome):
    """
    A class representing a web driver for scraping reviews.

    This class extends the functionality of the `webdriver.Chrome` class and provides additional methods
    and functionality specifically for scraping reviews.

    Args:
        executable_path (str): Path to the Chrome WebDriver executable.
        chrome_options (Options, optional): Chrome options to customize the WebDriver's behavior. Defaults to None.
        desired_capabilities (dict, optional): A dictionary of desired capabilities for the WebDriver. Defaults to None.
        service_log_path (str, optional): Path to the log file to capture service logs. Defaults to None.
        service_args (List[str], optional): List of additional arguments to pass to the WebDriver service.
        keep_alive (bool, optional): Whether to keep the WebDriver service alive after exiting the script.

    Usage:
        with Reviews(executable_path='path/to/chromedriver') as bot:
            bot.scrape_data()
        """

    def __init__(self, driver_path=r"C:\web_drivers\chromedriver", teardown=False):
        """
         Initialize the Reviews class.

        Args:
            driver_path (str): Path to the ChromeDriver executable.
                Default: 'C:\web_drivers\chromedriver'
            teardown (bool): Indicates whether to automatically close the WebDriver instance
                and quit the browser when the object is destroyed.
                Default: False
        """
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        super(Reviews, self).__init__(options=options)
        self.implicitly_wait(15)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager and perform necessary cleanup.

        Args:
            exc_type (type): The type of the exception raised, if any.
            exc_val (Exception): The exception instance raised, if any.
            exc_tb (traceback): The traceback object associated with the exception, if any.
        """
        if self.teardown:
            self.quit()

    def land_first_page(self):
        """
       Navigate to the review page specified by the user and load the review data.

       This method prompts the user to enter a review page URL.It then launches the specified review page in the browser
       and loads the review data by continuously clicking the "Load More" button until a maximum of 1000 review boxes
       have been loaded or until the "Load More" button is no longer interactable.

       Usage:
           bot = Reviews()
           bot.land_first_page()

       Raises:
           ElementNotInteractableException: If the "Load More" button becomes uninteractable before
           loading 1000 review boxes.

       Note:
           - The method assumes that the user will input a valid review page URL.
           - The WebDriver instance must be instantiated before calling this method.

        """

        review_page_link = input("Enter Review Page URL: ")
        self.get(review_page_link)
        time.sleep(1)
        progress_bar = tqdm(total=1000, desc='Loading Data')

        while True:
            review_boxes = self.find_elements(By.CLASS_NAME, "review-container")

            if not len(review_boxes) == 1000:
                try:
                    time.sleep(2)
                    load_more_button = self.find_element(By.ID, "load-more-trigger")
                    load_more_button.click()
                    progress_bar.update(len(review_boxes))

                except ElementNotInteractableException:
                    break

        progress_bar.close()

    def expander(self):
        """
       Expand the review sections on the page by clicking on the expand buttons.

       This method scrolls to the top of the page, finds all the expand buttons on the page, and clicks on each button
       in order to expand the corresponding review section. It waits for a short period after each click to allow the
       review section to expand before moving on to the next button.

       Usage:
           bot = Reviews()
           bot.expander()

       Note:
           - The WebDriver instance must be instantiated before calling this method.

        """
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        expander_buttons = self.find_elements(By.CSS_SELECTOR, 'div.expander-icon-wrapper.spoiler-warning__control')
        progress_bar = tqdm(total=len(expander_buttons), desc="Expanding Review Section")
        for button in expander_buttons:
            button.click()
            time.sleep(1)
            progress_bar.update(1)

        progress_bar.close()

    def name_extractor(self):
        """
            Extract the user_names associated with the reviews on the page.

            This method scrolls to the top of the page, finds all the user_name elements on the page, and extracts the
            user_names associated with the reviews. It returns a list of the extracted user_names.

            Usage:
                bot = Reviews()
                names = bot.name_extractor()
                for name in names:
                    print(name)

            Returns:
                list: A list of extracted user_names.

            Note:
                - The WebDriver instance must be instantiated before calling this method.

            """
        self.execute_script("window.scrollTo(0, 0);")
        user_name_elements = self.find_elements(By.CSS_SELECTOR, 'span[class="display-name-link"]')

        progress_bar = tqdm(total=len(user_name_elements), desc="Extracting User Names")

        names = []
        for user_name_element in user_name_elements:
            name_text = user_name_element.text.strip()
            names.append(name_text)

            progress_bar.update(1)
        progress_bar.close()

        return names

    def review_extractor(self):
        """
           Extract the text content of the review elements on the page.

           This method scrolls to the top of the page, finds all the review text elements on the page, and extracts the
           text content of each review element. It returns a list of the extracted review texts.

           Usage:
               bot = Reviews()
               reviews = bot.review_extractor()
               for review in reviews:
                   print(review)

           Returns:
               list: A list of extracted review texts.

           Note:
               - The WebDriver instance must be instantiated before calling this method.

           """
        self.execute_script("window.scrollTo(0, 0);")
        review_text_elements = self.find_elements(By.CSS_SELECTOR, 'div.content > div.text.show-more__control')

        progress_bar = tqdm(total=len(review_text_elements), desc="Extracting Reviews")
        reviews = []
        for review_element in review_text_elements:
            try:
                review_text = review_element.text.strip()
                reviews.append(review_text)
            except:
                reviews.append('N/A')

            progress_bar.update(1)

        progress_bar.close()

        return reviews

    def rating_extractor(self):
        """
           Extract the ratings associated with the reviews on the page.

           This method scrolls to the top of the page, finds all the rating elements on the page, and extracts the
           ratings associated with the reviews. It returns a list of the extracted ratings.

           Usage:
               bot = Reviews()
               ratings = bot.rating_extractor()
               for rating in ratings:
                   print(rating)

           Returns:
               list: A list of extracted ratings.

           Note:
               - The WebDriver instance must be instantiated before calling this method.

           """
        self.execute_script("window.scrollTo(0, 0);")
        rating_elements = self.find_elements(By.CSS_SELECTOR, 'div[class="lister-item-content"]')

        progress_bar = tqdm(total=len(rating_elements), desc="Extracting Ratings")
        ratings = []

        for rating_element in rating_elements:
            try:
                rating_value_element = rating_element.find_element(By.CSS_SELECTOR,
                                                                   'span.rating-other-user-rating span')
                rating_text = rating_value_element.text.strip()
                ratings.append(rating_text)
            except NoSuchElementException:
                ratings.append("N/A")

            progress_bar.update(1)
        progress_bar.close()

        return ratings

    def scrape_data(self):
        """
       Perform the complete data scraping process.

       This method executes the entire data scraping process, which includes landing on the first page,
       expanding the review sections, extracting user_names, reviews, and ratings,
       and saving the data to both a CSV file and an Excel file.

       Usage:
           bot = Reviews()
           bot.scrape_data()

       Note:
           - The WebDriver instance must be instantiated before calling this method.
           - The method assumes that the necessary file paths for saving the data to CSV and Excel files are provided.
           - The `save_to_excel` and `save_to_csv` functions are assumed to be defined and imported from elsewhere.
        """
        self.land_first_page()
        self.expander()
        names = self.name_extractor()
        reviews = self.review_extractor()
        ratings = self.rating_extractor()

        csv_file_path = r'C:\Users\Sandun Wijethunga\Documents\Workspace\Upwork\Web Scraping Projects\IMDB Movie Reviews\john_wick4_imdb_reviews_csv.csv'
        excel_file_path = r'C:\Users\Sandun Wijethunga\Documents\Workspace\Upwork\Web Scraping Projects\IMDB Movie Reviews\john_wick4_imdb_reviews_excel.xlsx'
        save_to_excel(names, reviews, ratings, excel_file_path)
        save_to_csv(names, reviews, ratings, csv_file_path)
        print("Scraping and saving completed. Job done!")
        self.teardown = True


if __name__ == "__main__":
    with Reviews() as bot:
        bot.scrape_data()
