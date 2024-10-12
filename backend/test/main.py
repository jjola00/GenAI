# main.py

from api_client import get_legal_advice

def main():
    print("Welcome to the Legal Advice Assistant.")
    
    while True:
        user_question = input("\nPlease enter your legal question (or type 'exit' to quit):\n")
        
        if user_question.lower() == "exit":
            print("Thank you for using the Legal Advice Assistant. Goodbye!")
            break
        
        # Call the function to get legal advice with relevant statutes
        advice = get_legal_advice(user_question)
        
        # Display the combined response from Perplexity and the Irish Statute Book
        print(f"\nAdvice:\n{advice}")

if __name__ == "__main__":
    main()

