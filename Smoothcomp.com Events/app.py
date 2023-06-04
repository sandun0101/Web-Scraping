from scraper.data_scraper import scrape_data
from utils.save_to_excel import save_to_excel

urls = [
    'https://smoothcomp.com/en/event/9910',
    'https://smoothcomp.com/en/event/9911',
    'https://smoothcomp.com/en/event/9912',
    'https://afbjj.smoothcomp.com/en/event/10416',
    'https://australian-taekwondo.smoothcomp.com/en/event/11304',
    'https://grapplingindustries.smoothcomp.com/en/event/11692',
    'https://smoothcomp.com/en/event/11516',
    'https://wrestling-australia.smoothcomp.com/en/event/11421',
    'https://smoothcomp.com/en/event/11276',
    'https://smoothcomp.com/en/event/11277',
    'https://smoothcomp.com/en/event/11735',
    'https://smoothcomp.com/en/event/10548',
    'https://smoothcomp.com/en/event/10551',
    'https://smoothcomp.com/en/event/9685',
    'https://compnet.smoothcomp.com/en/event/11305',
    'https://smoothcomp.com/en/event/10399'
]

# Scrape data
event_data = scrape_data(urls)

# Save data to Excel
excel_file = 'all_events.xlsx'
save_to_excel(event_data, excel_file)
