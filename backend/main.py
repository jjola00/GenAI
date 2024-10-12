import os
from flask import Flask, render_template, request
import spacy
from scraper import scrape_statute 

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
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True)
    else:
        user_input = input("Please enter your legal question: ")
        matched_laws = match_user_input_to_laws(user_input)
        if matched_laws:
            print(f"Found the following law(s): {matched_laws[0][0]}")
        else:
            print("No matching laws found.")

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
