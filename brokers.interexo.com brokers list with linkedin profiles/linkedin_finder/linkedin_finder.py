import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm


def create_retry_session():
    """
        Creates a session object with retry functionality for HTTP requests.

        Returns:
            requests.Session: Session object with retry functionality.

    """
    retry_strategy = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def find_linkedin_profiles(url_list):
    """
       Collects LinkedIn profile links from a list of URLs.

       Args:
           url_list (list): List of URLs to search for LinkedIn profile links.

       Returns:
           pd.DataFrame: DataFrame containing the LinkedIn profile links.

    """
    linkedin_links = []

    progress_bar = tqdm(total=len(url_list), desc='Collecting Linkedin Profiles')

    session = create_retry_session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }

    for url in url_list:
        if url == 'N/A':
            linkedin_links.append('N/A')
            continue

        try:
            response = session.get(url, headers=headers, timeout=5)
            response.raise_for_status()
        except (requests.RequestException, TimeoutError):
            linkedin_links.append('N/A')
            progress_bar.update(1)
            continue

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            anchor_tags = soup.find_all('a')

            linkedin_found = False
            for anchor in anchor_tags:
                href = anchor.get('href')
                if href:
                    linkedin_pattern = r"(?:https?://)?(?:www\.)?linkedin\.com/(?:in|company)/[a-zA-Z0-9_-]+/?"
                    match = re.search(linkedin_pattern, href)
                    if match:
                        linkedin_links.append(match.group(0))
                        linkedin_found = True
                        break

            if not linkedin_found:
                linkedin_links.append('N/A')
        else:
            linkedin_links.append('N/A')

        progress_bar.update(1)

    progress_bar.close()
    session.close()

    links = pd.DataFrame(linkedin_links)

    return links
