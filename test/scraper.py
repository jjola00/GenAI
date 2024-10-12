# scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_statute(query):
    """
    Scrapes the Irish Statute Book based on a given statute query.
    Example query: '2006/26' to get details about a specific statute.
    """
    base_url = "https://www.irishstatutebook.ie/eli/"
    url = f"{base_url}{query}/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        return None, f"Error fetching data: {e}"

    # Parse the response content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Adjust the selectors based on the HTML structure of the Irish Statute Book
    title = soup.find('h1')  # Find the title of the statute
    content = soup.find('div', class_='act-content')  # Find the content

    if title and content:
        return title.text.strip(), content.text.strip()  # Return title and content
    else:
        return None, "Statute not found. Please check your query."

# Example usage for testing:
if __name__ == "__main__":
    statute_title, statute_content = scrape_statute("2006/26")  # Replace with an actual statute number
    if statute_title:
        print("Title:", statute_title)
        print("Content:", statute_content)
    else:
        print(statute_content)

