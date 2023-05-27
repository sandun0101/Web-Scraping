from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.taskrabbit.com/profile/k-p/category/405')

reviewers = []

# Wait for the reviewers' elements to be present on the page
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-fHSyak.iHPqkj')))

max_iterations = 10
iteration = 0

while iteration < max_iterations:
    # Get the page source using Selenium
    page_source = driver.page_source

    # Create a BeautifulSoup object from the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    reviewer_elements = soup.find_all('div', class_='sc-kImNAt fMjDVx')

    for reviewer in reviewer_elements:
        reviewer_name_element = reviewer.find('div', class_='sc-jRwbcX bLnjzR')
        review_text_element = reviewer.find('div', class_='sc-jTjUTQ hWqDzL')

        reviewer_name = reviewer_name_element.text if reviewer_name_element else "N/A"
        review_text = review_text_element.text if review_text_element else "No review available"

        reviewers.append({'Reviewer': reviewer_name, 'Review': review_text})

    # Find and click the next button
    next_button = driver.find_element(By.CSS_SELECTOR, 'i.ss-caret-right')
    next_button.click()

    iteration += 1

for reviewer in reviewers:
    reviewer_name = reviewer['Reviewer']
    review_text = reviewer['Review']
    print(f"Reviewer: {reviewer_name}")
    print(f"Review: {review_text}")
    print("----------------------")

driver.quit()
