import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import pdfplumber
from api_client import get_legal_advice
from utils import validate_input

app = Flask(__name__)

# Irish Statute Book URL
BASE_URL = 'http://www.irishstatutebook.ie'
SAVE_DIRECTORY = 'irish_statute_pdfs'
LIST_URL = 'http://www.irishstatutebook.ie/eli/acts.html'

# Gets act list from Irish Statute Book
def get_acts_list(list_url):
    return []

#Get PDF Link
def get_pdf_link(act_url):
    return None

# Downloads PDF
def download_pdf(pdf_url, save_directory):
    pass

#Extracts text
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

def cli_main():
    user_input = input("Please enter your legal question: ")

    if validate_input(user_input):
        response = get_legal_advice(user_input)
        print("Response:", response)
    else:
        print("Invalid input. Please try again.")

def main():
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True)
    else:
        cli_main()

if __name__ == "__main__":
    main()
