# main.py

from api_client import get_legal_advice
from utils import validate_input

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
