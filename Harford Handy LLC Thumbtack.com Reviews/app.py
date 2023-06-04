import csv
from utils.selenium_utils import SeleniumScraper
from scraper.data_processing import get_full_review_text, filter_empty_reviews, create_data_dict
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import utils.constants as const


def scrape_reviews(url):
    scraper = SeleniumScraper()
    scraper.get_page_content(url)

    data = []

    while True:
        name_elements = scraper.wait_for_elements((By.CSS_SELECTOR, 'div._1IFLvn772QsHli5N5sL9V1'))
        review_elements = scraper.wait_for_elements((By.CSS_SELECTOR, 'div.pre-line._35bESqM0YmWdRBtN-nsGpq'))

        reviewer_names = [scraper.find_element_text(name_element) for name_element in name_elements]
        reviews = []

        for review_element in review_elements:
            full_review_text = get_full_review_text(scraper, review_element)
            if full_review_text:
                reviews.append(full_review_text)

        filtered_reviews = filter_empty_reviews(reviews)
        data.extend(create_data_dict(reviewer_names, filtered_reviews))

        try:
            next_button = scraper.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'vIRQFgYANCphKO9-RQaWv') and contains(@aria-label, 'Next')]")))
        except TimeoutException:
            break

        if next_button:
            scraper.click_element(next_button)
            scraper.wait.until(EC.staleness_of(name_elements[0]))
        else:
            break

    scraper.close_browser()
    return data


def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(data)


data = scrape_reviews(const.BASE_URL)
save_to_csv(data, 'reviews.csv')
print('Data is saved to csv file...')
