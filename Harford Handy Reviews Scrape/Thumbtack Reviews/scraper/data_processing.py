from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def get_full_review_text(scraper, review_element):
    try:
        read_more_button = review_element.find_element(By.CSS_SELECTOR, 'button._230fLSlginFVu7q_SLOkRk._2uwAL44FcBnDRususT6gtq')
        scraper.click_element(read_more_button)
    except NoSuchElementException:
        pass
    return scraper.find_element_text(review_element)


def filter_empty_reviews(reviews):
    return [review for review in reviews if review]


def create_data_dict(reviewer_names, reviews):
    return [{'Reviewer Name': name, 'Review': review} for name, review in zip(reviewer_names, reviews)]
