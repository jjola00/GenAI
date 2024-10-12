import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import PyPDF2
import time
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError

# Folder to store downloaded PDFs
output_folder = 'legal_documents'

# Create the folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Set to keep track of visited URLs
visited_urls = set()

def is_valid_url(url, base_url):
    # Ensure the URL is internal to the Irish Statute Book
    return urlparse(url).netloc == '' or urlparse(url).netloc == urlparse(base_url).netloc

def download_pdf(pdf_url):
    # Get the filename by splitting the URL
    pdf_filename = pdf_url.split('/')[-1]
    
    # Send a request to download the PDF file
    try:
        pdf_response = requests.get(pdf_url, timeout=10)  # 10 seconds timeout
        pdf_response.raise_for_status()  # Ensure the request was successful
        
        # Save the PDF to the output folder
        pdf_path = os.path.join(output_folder, pdf_filename)
        with open(pdf_path, 'wb') as f:
            f.write(pdf_response.content)
        
        print(f"Downloaded: {pdf_filename}")
        
        # Extract text from the downloaded PDF
        extract_text_from_pdf(pdf_path)
        
    except (ConnectTimeout, ReadTimeout, ConnectionError) as e:
        print(f"Connection error while downloading {pdf_url}: {e}")
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        print(f"Extracted text from: {pdf_path}")
        
        # Save the extracted text to a .txt file (optional)
        text_filename = pdf_path.replace('.pdf', '.txt')
        with open(text_filename, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
    except Exception as e:
        print(f"Failed to extract text from {pdf_path}: {e}")

def crawl_website(url, base_url):
    if url in visited_urls:
        return  # Skip if the URL has been visited

    visited_urls.add(url)  # Mark the URL as visited
    
    try:
        # Send a request to fetch the HTML of the page with a timeout
        response = requests.get(url, timeout=10)  # 10 seconds timeout
        response.raise_for_status()  # Ensure the request was successful
    except (ConnectTimeout, ReadTimeout, ConnectionError) as e:
        print(f"Connection error with {url}: {e}")
        return  # Skip this URL and continue with the next one
    except Exception as e:
        print(f"Failed to retrieve {url}. Error: {e}")
        return
    
    # If the request is successful, parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <a> tags that have an href attribute
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        
        # Handle relative URLs
        full_url = urljoin(base_url, href)
        
        # If the link is a PDF, download it
        if full_url.endswith('.pdf'):
            download_pdf(full_url)
        
        # If the link is an internal link (within the same domain), crawl it
        elif is_valid_url(full_url, base_url):
            crawl_website(full_url, base_url)
    
    # Sleep for a while before making the next request to avoid overwhelming the server
    time.sleep(1)  # Wait for 1 second between requests

# Starting point: main URL of Irish Statute Book
website_url = 'https://www.irishstatutebook.ie'

# Start crawling from the base URL
crawl_website(website_url, website_url)

