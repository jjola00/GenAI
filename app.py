from flask import Flask, render_template, jsonify, request
from api_client import get_legal_advice
from utils import validate_input
import lawyerFinder

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

user_input = ""

def GetResponse(inp):
    user_input = inp
    # Validate user input
    if validate_input(user_input):
        response = get_legal_advice(user_input)
        return response
    else:
        return "Invalid input. Please try again."
@app.route('/generate/<inp>')
def generate(inp):
    response = GetResponse(inp)
    return response

@app.route('/get/lawyers/<tags>')
def GetAllLawyersWithTags(tags):
    client = lawyerFinder.LawyerFinder(tags)
    client.saveLawyersWithCorrectTags()
    return jsonify(client.lawyers)

def main():
    user_input = input("Please enter your legal question: ")
    # Validate user input
    if validate_input(user_input):
        response = get_legal_advice(user_input)
        print("Response:", response)
    else:
        print("Invalid input. Please try again.")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)