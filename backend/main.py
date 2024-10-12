import os
from flask import Flask, render_template, request
import spacy
from scraper import scrape_statute 
from api_client import get_legal_advice
from utils import validate_input

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Analyze user input
def analyze_user_input(user_input):
    doc = nlp(user_input)
    # Extract relevant nouns or verbs
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'VERB']]
    return keywords

# Match user input with relevant laws using the scraper
def match_user_input_to_laws(user_input):
    keywords = analyze_user_input(user_input)
    if keywords:
        # Using the first relevant keyword for now
        law_title, law_content = scrape_statute(keywords[0])
        if law_content != "Statute not found.":
            return [(law_title, law_content)]
        else:
            return None
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_query():
    user_input = request.form['user_input']
    matched_laws = match_user_input_to_laws(user_input)

    if matched_laws:
        return render_template('results.html', results=matched_laws)
    else:
        return render_template('results.html', error="No matching laws found.")

user_input = ""

def main():
    user_input = input("Please enter your legal question: ")
    
    # Validate user input
    if validate_input(user_input):
        response = get_legal_advice(user_input)
        print("Response:", response)
    else:
        print("Invalid input. Please try again.")

def GetResponse(inp):
    user_input = inp
    
    # Validate user input
    if validate_input(user_input):
        response = get_legal_advice(user_input)
        #print("Response:", response)
        return response
    else:
        #print("Invalid input. Please try again.")
        return "Invalid input. Please try again."

if __name__ == "__main__":
    #main()
    pass
