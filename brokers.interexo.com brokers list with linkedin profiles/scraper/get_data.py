import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from linkedin_finder.linkedin_finder import find_linkedin_profiles


def data_scraper(url_list):
    """
        Scrapes data from a list of URLs.

        Args:
            url_list (list): List of URLs to scrape data from.

        Returns:
            pd.DataFrame: DataFrame containing the scraped data.

    """
    broker_names = []
    company_names = []
    company_address = []
    company_phone = []
    description = []
    emails = []
    websites = []

    progress_bar = tqdm(total=len(url_list), desc='Collecting data')

    for url in url_list:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')

        broker_name = soup.find('h1', attrs={'class': 'company-name'}).text.strip()
        broker_names.append(broker_name)

        company_name = soup.find('div', attrs={'class': 'col-auto'})
        name = company_name.find('a').text.strip()
        company_names.append(name)

        address_line1 = soup.find_all('div', attrs={'class': 'pt-1'})
        address = address_line1[0].text.strip()
        company_address.append(address)

        try:
            phone_number = soup.select('.pt-1')[-1].text.strip()
            number = re.findall(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", phone_number)
            if len(number) > 0:
                num = str(number).strip('[]\'')
                company_phone.append(num)
            else:
                company_phone.append('N/A')
        except:
            company_phone.append('N/A')

        broker_description = soup.find('div', class_="row pt-4 company-description").text.strip()
        description.append(broker_description)

        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
            email_address = soup.find_all('div', class_="pt-3")
            email = re.findall(email_pattern, email_address[1].text.strip())
            stripped_email = str(email).strip('[]\'')
            emails.append(stripped_email)
        except:
            emails.append('N/A')

        try:
            website_pattern = r"https?://([\w.-]+)"
            website_element = soup.find('div', class_='col-auto').find('a', href=re.compile(r'https?://'))
            website = re.search(website_pattern, website_element['href']).group(0)
            websites.append(website)
        except:
            websites.append('N/A')

        progress_bar.update(1)
    progress_bar.close()

    data = {
        'Broker Name': broker_names,
        'Company Name': company_names,
        'Company Address': company_address,
        'Company Phone': company_phone,
        'Description': description,
        'Email': emails,
        'Website': websites
    }

    df = pd.DataFrame(data)

    websites_urls = df['Website'].to_list()
    linkedin_links = find_linkedin_profiles(websites_urls)

    df['Linkedin Profile'] = linkedin_links

    return df






