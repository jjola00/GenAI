import os
import openai  # or the relevant library for the LLM you are using


def main():
    # Load extracted texts
    extracted_texts = load_extracted_texts('legal_documents')

    # User input
    user_prompt = input("Enter your query regarding the legal document: ")

    # Iterate over each document and get advice
    for text in extracted_texts:
        advice = get_legal_advice(text, user_prompt)
        print(advice)

if __name__ == "__main__":
    main()

