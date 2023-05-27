import csv
from utils.selenium_utils import SeleniumScraper
from scraper.data_processing import get_full_review_text, filter_empty_reviews, create_data_dict
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def scrape_reviews(url):
    scraper = SeleniumScraper()
    scraper.get_page_content(url)

    data = []

    while True:
        name_elements = scraper.wait_for_elements((By.CSS_SELECTOR, 'div._1IFLvn772QsHli5N5sL9V1'))
        review_elements = scraper.wait_for_elements((By.CSS_SELECTOR, 'div.pre-line'))

        reviewer_names = [scraper.find_element_text(name_element) for name_element in name_elements]
        reviews = []

        for review_element in review_elements:
            full_review_text = get_full_review_text(scraper, review_element)
            if full_review_text:
                reviews.append(full_review_text)

        filtered_reviews = filter_empty_reviews(reviews)
        data.extend(create_data_dict(reviewer_names, filtered_reviews))

        # Check if the "Next" button is clickable
        try:
            next_button = scraper.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'vIRQFgYANCphKO9-RQaWv') and contains(@aria-label, 'Next')]")))
        except TimeoutException:
            # No more pages, break out of the loop
            break

        if next_button:
            scraper.click_element(next_button)
            scraper.wait.until(EC.staleness_of(name_elements[0]))
        else:
            # No more pages, break out of the loop
            break

    scraper.close_browser()
    return data


def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(data)

# Usage example
url = 'https://www.thumbtack.com/md/havre-de-grace/handyman/harford-handy-llc/service/440736644627759105?from_native_webview=true&supports_redirect_ttevent=true&native_app_name=com.thumbtack.wingtip&native_app_build=8470&native_app_version=306.0&native_os_version=16.4.1&native_device_type=iPhone14%'
data = scrape_reviews(url)
save_to_csv(data, 'reviews.csv')
print('Data is saved to csv file...')
