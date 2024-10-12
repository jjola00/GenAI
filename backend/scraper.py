# scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_statute(query):
    # Modify this URL to match the correct format for the Irish Statute Book
    url = f"https://www.irishstatutebook.ie/eli/{query}"  
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').text  # Adjust based on actual HTML structure
        content = soup.find('div', class_='act-content').text  # Adjust based on actual HTML structure
        return title, content
    else:
        return None, "Statute not found."

scrape_statute("Rape")
