import requests
import json
import re
from bs4 import BeautifulSoup


def scrape_data(urls):
    """
    Scrapes event data from a list of URLs.
    Args:
        urls (list): A list of URLs to scrape data from.

    Returns:
        dict: A dictionary containing the scraped event data with the following keys:
             - 'Event Name': List of event names
            - 'Event Date': List of event dates
            - 'Age Bracket': List of age brackets
            - 'Event Location': List of event locations
            - 'Organizing Company': List of organizing company names
            - 'Organizer City': List of organizer city names
            - 'Organizer Country': List of organizer country names
            - 'Organizer Email': List of organizer email addresses
    """
    event_data = {
        'Event Name': [],
        'Event Date': [],
        'Age Bracket': [],
        'Event Location': [],
        'Organizing Company': [],
        'Organizer City': [],
        'Organizer Country': [],
        'Organizer Email': []
    }

    for url in urls:
        page_content = requests.get(url).content
        soup = BeautifulSoup(page_content, 'html.parser')

        # Getting event and organizer details
        script_tag = soup.find('script', {'type': 'application/ld+json'})

        if script_tag:
            json_data = script_tag.string
            data = json.loads(json_data)

            event_name = data['name']
            event_location_name = data["location"]["address"]["description"]
            event_date = data['startDate']
            organizer_company = data['organizer']['name']
            organizer_city = data['location']['address']['addressLocality']
            organizer_country = data['location']['address']['addressCountry']

        # Find email from the website
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        byte_content = page_content.decode('utf-8')
        email_list = re.findall(email_pattern, byte_content)

        for email in email_list:
            print(email)

        age_limits = []
        age_bracket = soup.find_all('li', class_='list-group-item')

        for item in age_bracket:
            age_limit = item.text.split('\n')[1].strip()
            age_limits.append(age_limit)

        # Create a list of age limits separated by commas
        age_limits_str = ', '.join(age_limits)

        # Append the details to the event_data dictionary
        event_data['Event Name'].append(event_name)
        event_data['Event Date'].append(event_date)
        event_data['Age Bracket'].append(age_limits_str)
        event_data['Event Location'].append(event_location_name)
        event_data['Organizing Company'].append(organizer_company)
        event_data['Organizer City'].append(organizer_city)
        event_data['Organizer Country'].append(organizer_country)
        event_data['Organizer Email'].append(email)

    return event_data
