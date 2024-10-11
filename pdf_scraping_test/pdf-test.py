#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the website to scrape (Replace with the actual website URL)
website_url = 'https://www.irishstatutebook.ie'

# Folder to store downloaded PDFs
output_folder = 'pdf_files'

# Create the folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Send a request to fetch the HTML of the website
response = requests.get(website_url)

# Ensure the request was successful
if response.status_code == 200:
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags that have an href attribute
    pdf_links = soup.find_all('a', href=True)

    # Counter to track how many PDFs were downloaded
    pdf_count = 0

    # Filter out the links that end with '.pdf'
    for link in pdf_links:
        pdf_url = link['href']

        # Handle relative URLs
        full_pdf_url = urljoin(website_url, pdf_url)

        # Check if the URL ends with '.pdf'
        if full_pdf_url.endswith('.pdf'):
            # Get the filename by splitting the URL
            pdf_filename = full_pdf_url.split('/')[-1]

            # Send a request to download the PDF file
            pdf_response = requests.get(full_pdf_url)

            # Save the PDF to the output folder
            pdf_path = os.path.join(output_folder, pdf_filename)
            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)

            print(f"Downloaded: {pdf_filename}")
            pdf_count += 1

    if pdf_count == 0:
        print("No PDFs found on the page.")
    else:
        print(f"Total PDFs downloaded: {pdf_count}")
else:
    print(f"Failed to retrieve the website. Status code: {response.status_code}")
