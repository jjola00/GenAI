import os
#run pip install requests, pip install flask, pip install pdfplumber and pip install beautifulsoup4
import requests
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import pdfplumber

app = Flask(__name__)

#Irish Statute Book URL
BASE_URL = 'http://www.irishstatutebook.ie'


SAVE_DIRECTORY = 'irish_statute_pdfs'

# URL of the page that lists the acts
LIST_URL = 'http://www.irishstatutebook.ie/eli/acts.html'

def get_acts_list(list_url):
        return []

def get_pdf_link(act_url):
        return None

def download_pdf(pdf_url, save_directory):
        pass

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            full_text += text if text else ""
    return full_text

@app.route('/')
def index():
    return render_template('index.html')

def main():
    pass

if __name__ == "__main__":
    app.run(debug=True)
