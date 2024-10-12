import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import pdfplumber
from api_client import get_legal_advice
from utils import validate_input
import spacy

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
def extract_all_pdfs(directory):
    all_text = {}
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                all_text[filename] = text
    return all_text

#Searches for laws
def search_laws(keyword, extracted_texts):
    results = []
    for title, text in extracted_texts.items():
        if keyword.lower() in text.lower():
            results.append((title, text))
    return results

# Loads spacy's english model
nlp = spacy.load("en_core_web_sm")

# Analyze user input for key terms
def analyze_user_input(user_input):
    doc = nlp(user_input)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'VERB']]
    return keywords

def match_user_input_to_laws(user_input, extracted_texts):
    keywords = analyze_user_input(user_input)
    matched_laws = []
    
    for keyword in keywords:
        results = search_laws(keyword, extracted_texts)
        matched_laws.extend(results)
    
    return matched_laws

extracted_texts = extract_all_pdfs(SAVE_DIRECTORY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_query():
    user_input = request.form['user_input']
    matched_laws = match_user_input_to_laws(user_input, extracted_texts)
    return render_template('results.html', results=matched_laws)

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
