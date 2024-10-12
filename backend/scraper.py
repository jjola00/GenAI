#scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_statute(query):
    search_url = f"https://www.irishstatutebook.ie/search.html?q={query}" 
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse the first matching act link
        first_result = soup.find('a', class_='search-result')
        if first_result:
            act_url = "https://www.irishstatutebook.ie" + first_result['href']
            return fetch_act_content(act_url)
        else:
            return None, "No relevant statute found for this query."
    else:
        return None, "Failed to fetch search results."

def fetch_act_content(act_url):
    response = requests.get(act_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1').text  # Title of the act
        content = soup.find('div', class_='act-content').text  # Main content of the act
        return title, content
    else:
        return None, "Statute not found."
