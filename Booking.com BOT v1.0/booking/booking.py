import os
import time
import booking.constants as const
from tqdm import tqdm
from selenium import webdriver
from prettytable import PrettyTable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from booking.booking_filtration import BookingFiltration
from selenium.webdriver.support import expected_conditions as EC


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\web_drivers\chromedriver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            print('quit')
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        print("Navigating....")

    def dismiss_signin_info(self):
        wait = WebDriverWait(self, 10)
        closing_button = wait.until(
            EC.element_to_be_clickable((
                By.CLASS_NAME,
                "fc63351294.a822bdf511.e3c025e003.fa565176a8.f7db01295e.c334e6f658.ae1678b153"
                                        )))

        closing_button.click()

    def change_currency(self, currency=None):
        wait = WebDriverWait(self, 10)
        currency_element = wait.until(
            EC.element_to_be_clickable((
                By.CLASS_NAME,
                "fc63351294.a822bdf511.e3c025e003.cfb238afa1.c334e6f658.e634344169"
                                        )))

        currency_element.click()

    def select_currency(self):
        wait = WebDriverWait(self, 10)
        select_button = wait.until(EC.element_to_be_clickable((
            By.CLASS_NAME,
            "fc63351294.ea925ef36a.bf97d4018a.ae8177da1f.cddb75f1fd"
                                                               )))

        select_button.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.NAME, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        time.sleep(3)
        results_list = self.find_element(By.CLASS_NAME, 'a80e7dc237')
        results_list.click()

    def select_dates(self, check_in_date, check_out_date):
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

    def select_adult_count(self, count=1):
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

        for _ in range(count-1):
            adult_increase_button.click()

    def select_room_count(self, count=1):
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
        if int(current_room_count) == 1:
            for _ in range(count-1):
                room_count_button.click()

    def search_data(self):
        search_button = self.find_element(
            By.CLASS_NAME,
            "fc63351294.a822bdf511.d4b6b7a9e7.cfb238afa1.c938084447.f4605622ad.aa11d0d5cd"
        )

        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.sort_lowest_price_first()
        filtration.apply_star_rating(star_value=5)
        time.sleep(3)

    def scraper(self):
        offer_boxes = self.find_elements(By.CLASS_NAME, "b978843432")

        boxes_len = len(offer_boxes)
        progress_bar = tqdm(total=boxes_len, desc="Collecting Data..")

        table = PrettyTable(["Hotel Name", "Hotel Address", "Hotel Score", "Room Type", "Price"])

        for offer_box in offer_boxes:
            hotel_name = offer_box.find_element(
                By.CSS_SELECTOR, 'a.e13098a59f > div.fcab3ed991.a23c043802').text.strip()

            hotel_address = offer_box.find_element(By.CSS_SELECTOR,'span.f4bd0794db.b4273d69aa').text.strip()

            hotel_score = offer_box.find_element(By.CSS_SELECTOR, 'div.b5cd09854e.d10a6220b4').text

            hotel_room_type = offer_box.find_element(By.CSS_SELECTOR, 'span.df597226dd').text.strip()

            hotel_price = offer_box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text

            table.add_row([hotel_name, hotel_address, hotel_score, hotel_room_type, hotel_price])

            progress_bar.update(1)

        progress_bar.close()

        print("Completed..")
        print(table)







