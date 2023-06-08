import pandas as pd
from scraper.get_data import data_scraper

try:
    url_df = pd.read_csv('brokers_links.csv')
    url_list = url_df['Links'].to_list()

    results = data_scraper(url_list)

    results.to_excel('company_details.xlsx', index=False)

except Exception as e:
    raise
