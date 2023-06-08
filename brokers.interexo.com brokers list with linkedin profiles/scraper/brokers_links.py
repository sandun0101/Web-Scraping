import requests
import pandas as pd
from bs4 import BeautifulSoup

base_url = "https://brokers.interexo.com/"


def brokers_page_links(domain_url):
    links = []
    for page_number in range(1, 18):
        url = f"https://brokers.interexo.com/search?country%5B0%5D=United%20States&state%5B0%5D=New%20York&page={page_number}"
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        brokers_link = soup.find_all('div', attrs={"class": "col pe-1"})

        for link in brokers_link:
            href_link = link.find('a')['href']
            full_link = base_url + href_link
            links.append(full_link)

    df = pd.DataFrame(links, columns=['Links'])
    df.to_csv('links.csv', index=False)


brokers_page_links(base_url)




