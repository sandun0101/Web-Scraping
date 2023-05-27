from utils.taskrabbit import TaskRabbit
from selenium.webdriver.common.by import By

with TaskRabbit() as bot:
    bot.land_first_page()
    for element in bot.report_result():
        name = element.find_element(By.CSS_SELECTOR, 'div.sc-jRwbcX.bLnjzR').text.strip()
        print(name)


