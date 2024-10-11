import os
#run pip install requests and pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup

#Irish Statute Book URL
BASE_URL = 'http://www.irishstatutebook.ie'


SAVE_DIRECTORY = 'irish_statute_pdfs'

# URL of the page that lists the acts
LIST_URL = 'http://www.irishstatutebook.ie/eli/acts.html'

def get_acts_list(list_url):
    try:
        response = requests.get(list_url)
        response.raise_for_status()  # Check for errors
        soup = BeautifulSoup(response.text, 'html.parser')
        # Finds all links to acts pages
        acts_links = soup.find_all('a', href=True)
        return acts_links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching list of acts: {e}")
        return []

def get_pdf_link(act_url):
    try:
        response = requests.get(act_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Finds link to PDF file
        pdf_link = soup.find('a', href=lambda href: href and href.endswith('.pdf'))
        if pdf_link:
            return BASE_URL + pdf_link['href']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PDF link for {act_url}: {e}")
        return None

def download_pdf(pdf_url, save_directory):
    try:
        pdf_name = pdf_url.split('/')[-1]
        pdf_path = os.path.join(save_directory, pdf_name)
        
        response = requests.get(pdf_url)
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        
        print(f"Downloaded: {pdf_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {pdf_url}: {e}")

def main():
    # Gets link of acts
    acts_links = get_acts_list(LIST_URL)

    # Loops through each act link
    for link in acts_links:
        act_url = BASE_URL + link['href']
        print(f"Processing Act: {act_url}")
        
        # Get the PDF link from the act page
        pdf_url = get_pdf_link(act_url)

        if pdf_url:
            # Downloads the PDF
            download_pdf(pdf_url, SAVE_DIRECTORY)
        else:
            print(f"No PDF found for: {act_url}")

if __name__ == "__main__":
    main()
