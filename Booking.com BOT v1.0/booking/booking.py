import os
import time
import datetime
import booking.constants as const
from tqdm import tqdm
from selenium import webdriver
from prettytable import PrettyTable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from booking.booking_filtration import BookingFiltration
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class Booking(webdriver.Chrome):
    """
    A custom subclass of webdriver.Chrome for automating the Booking.com website.
    This class extends the webdriver.Chrome class from the Selenium library to provide additional
    functionality and convenience methods specific to interacting with the Booking.com website.
    """
    def __init__(self, driver_path=r"C:\web_drivers\chromedriver", teardown=False):
        """
         Initialize the Booking class.

        Args:
            driver_path (str): Path to the ChromeDriver executable.
                Default: "C:\web_drivers\chromedriver"
            teardown (bool): Indicates whether to automatically close the WebDriver instance
                and quit the browser when the object is destroyed.
                Default: False
        """
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("detach", True)
        super(Booking, self).__init__()
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
        Navigate to the landing page of the Booking.com website.
        This method launches the Booking.com website in the browser and lands on the initial page.
        """
        self.get(const.BASE_URL)
        print("Navigating....")

    def dismiss_signin_info(self):
        """
        Dismiss the sign-in information or pop-up on the Booking.com website.
        This method is used to handle and dismiss any sign-in information or pop-up that might appear on the Booking.com website.
        It is helpful when automating interactions on the website to ensure smooth navigation and avoid interruptions.
        """
        wait = WebDriverWait(self, 10)
        closing_button = wait.until(
            EC.element_to_be_clickable((
                By.CLASS_NAME,
                "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.ae1678b153"
            )))

        closing_button.click()

    def currency_list(self):
        """
          Get the list of available currencies on the Booking.com website.
          This method retrieves the list of available currencies that can be used for currency conversion
          on the Booking.com website.
        """
        wait = WebDriverWait(self, 10)
        currency_element = wait.until(
            EC.element_to_be_clickable((
                By.CLASS_NAME,
                "fc63351294.a822bdf511.e3c025e003.cfb238afa1.c334e6f658.e634344169"
            )))

        currency_element.click()

    def select_currency(self):
        """
         Select the currency for the Booking.com website.
         This method allows the user to select a currency from the available options on the Booking.com website.
        """
        currency_elements = self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')

        while True:
            choice = input("Enter Currency(USD,EUR,GBP): ").upper()
            match choice:
                case "EUR":
                    eur_button = currency_elements[22]
                    eur_button.click()
                case "USD":
                    usd_button = currency_elements[55]
                    usd_button.click()
                case "GBP":
                    gbp_button = currency_elements[43]
                    gbp_button.click()
                case _:
                    print("Invalid Input. please choose currency from USD, EUR, GBP")

    def select_place_to_go(self):
        """
        Select the desired place to go on the Booking.com website.
        This method allows the user to select a specific place or destination they want to visit on the Booking.com website.
        """
        place_to_go = input("Enter the location: ")
        search_field = self.find_element(By.NAME, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        time.sleep(3)
        results_list = self.find_element(By.CLASS_NAME, 'a80e7dc237')
        results_list.click()

    def select_dates(self):
        """
        Prompt the user to enter check-in and check-out dates, and select them on the Booking.com website.
        This method interacts with the user to input the desired check-in and check-out dates in the format 'YYYY-MM-DD'.
        It validates the date range and selects the corresponding dates on the Booking.com website using the date picker.
        """
        while True:
            check_in_date = input("Enter the check-in date (YYYY-MM-DD): ")
            check_out_date = input("Enter the check-out date (YYYY-MM-DD): ")

            try:
                check_in = datetime.datetime.strptime(check_in_date, "%Y-%m-%d")
                check_out = datetime.datetime.strptime(check_out_date, "%Y-%m-%d")

                if check_out >= check_in:
                    break

                else:
                    print("Invalid date range. Check-out date should be after or equal to the check-in date.")
            except ValueError:
                print("Invalid date format. Please enter dates in the format YYYY-MM-DD.")

        wait = WebDriverWait(self, 10)
        date_picker = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "f92dfc7e1a")))

        check_in_month, check_in_day = check_in_date.split("-")[1:]
        check_out_month, check_out_day = check_out_date.split("-")[1:]

        check_in_locator = f'[data-date="2023-{check_in_month.zfill(2)}-{check_in_day.zfill(2)}"]'
        check_in_element = date_picker.find_element(By.CSS_SELECTOR, check_in_locator)
        check_in_element.click()

        check_out_locator = f'[data-date="2023-{check_out_month.zfill(2)}-{check_out_day.zfill(2)}"]'
        check_out_element = date_picker.find_element(By.CSS_SELECTOR, check_out_locator)
        check_out_element.click()

    def select_people_count(self):
        """
        Select the number of people for the booking on the Booking.com website.
        This method interacts with the user to input the desired number of people for the booking.
        It selects the corresponding number of adults on the Booking.com website using the increase button.
        """
        selection_element = self.find_element(By.CLASS_NAME, "d47738b911.b7d08821c3")
        selection_element.click()

        while True:
            adult_decrease_button = self.find_element(
                By.CSS_SELECTOR,
                "button.fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.e1b7cfea84.cd7aa7c891"
            )
            adult_decrease_button.click()

            adult_count_element = self.find_element(By.CSS_SELECTOR, "span.e615eb5e43").text.strip()

            if int(adult_count_element) == 1:
                break

        adult_increase_button = self.find_element(
            By.CSS_SELECTOR,
            "button.fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.e1b7cfea84.d64a4ea64d"
        )
        people_count = int(input("Enter how many people: "))

        for _ in range(people_count - 1):
            adult_increase_button.click()

    def select_room_count(self):
        """
        Select the number of rooms for the booking on the Booking.com website.
        This method interacts with the user to input the desired number of rooms for the booking.
        It selects the corresponding number of rooms on the Booking.com website using the increase button.
        """
        selection_buttons = self.find_elements(
            By.CLASS_NAME,
            "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.e1b7cfea84.d64a4ea64d"
        )

        room_count_button = selection_buttons[-1]

        current_count_elements = self.find_elements(
            By.CLASS_NAME,
            "e615eb5e43"
        )

        current_room_count = current_count_elements[-1].text.strip()
        room_count = int(input("Enter how many rooms: "))

        if int(current_room_count) == 1:
            for _ in range(room_count - 1):
                room_count_button.click()

    def search_data(self):
        """
        Initiate the search for data on the Booking.com website.
        This method performs the action of clicking the search button on the Booking.com website
        to initiate the search for the specified data (e.g., hotels, accommodations).
        """
        search_button = self.find_element(
            By.CLASS_NAME,
            "fc63351294.a822bdf511.d4b6b7a9e7.cfb238afa1.c938084447.f4605622ad.aa11d0d5cd"
        )

        search_button.click()

    def apply_filtrations(self):
        """
        Apply filtrations to refine the search results on the Booking.com website.
        This method applies filtrations to the search results on the Booking.com website to refine and narrow down the results.
        It uses the `BookingFiltration` class to perform specific filtrations, such as sorting by lowest price first
        and applying a star rating filter.
        """
        filtration = BookingFiltration(driver=self)
        filtration.sort_lowest_price_first()
        filtration.apply_star_rating(star_value=5)
        time.sleep(3)

    def scraper(self):
        """
         Scrape and collect data from the search results on the Booking.com website.
         This method scrapes and collects data from the offer boxes in the search results on the Booking.com website.
         It retrieves information such as hotel name, address, score, room type, and price.
         The collected data is displayed in a formatted table using the `PrettyTable` library.
         If the hotel score is not available for a particular offer box, it is assigned the value "N/A".
        """
        time.sleep(3)
        offer_boxes = self.find_elements(By.CLASS_NAME, "b978843432")

        boxes_len = len(offer_boxes)
        progress_bar = tqdm(total=boxes_len, desc="Collecting Data..")

        table = PrettyTable(["Hotel Name", "Hotel Address", "Hotel Score", "Room Type", "Price"])

        for offer_box in offer_boxes:
            hotel_name = offer_box.find_element(
                By.CSS_SELECTOR, 'a.e13098a59f > div.fcab3ed991.a23c043802').text.strip()

            hotel_address = offer_box.find_element(By.CSS_SELECTOR, 'span.f4bd0794db.b4273d69aa').text.strip()

            try:
                hotel_score = offer_box.find_element(By.CSS_SELECTOR, 'div.b5cd09854e.d10a6220b4').text
            except NoSuchElementException:
                hotel_score = "N/A"

            hotel_room_type = offer_box.find_element(By.CSS_SELECTOR, 'span.df597226dd').text.strip()

            hotel_price = offer_box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text

            table.add_row([hotel_name, hotel_address, hotel_score, hotel_room_type, hotel_price])

            progress_bar.update(1)

        progress_bar.close()

        print("Completed..")
        print(table)

        self.teardown = True
