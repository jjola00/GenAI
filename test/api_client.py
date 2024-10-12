# api_client.py

import requests
from scraper import scrape_statute

API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = "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"  # Replace with your API key

def get_legal_advice(user_question):
    # Prepare the request payload for the Perplexity API
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "Provide concise legal advice."},
            {"role": "user", "content": user_question}
        ],
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_citations": True,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Send the request to the Perplexity API
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        api_response = response.json()
    except requests.RequestException as e:
        return f"Error with Perplexity API: {e}"

    # Extract the API-generated response
    generated_response = api_response['choices'][0]['message']['content']

    # Here, you can extract keywords or manually pass a relevant query for scraping
    statute_query = "2006/26"  # Example placeholder, replace with logic to extract statute number

    # Call the scraper to get relevant statute information
    statute_title, statute_content = scrape_statute(statute_query)

    # Return combined response from Perplexity and scraped legal content
    if statute_title:
        return f"{generated_response}\n\nLegal Reference:\n\nTitle: {statute_title}\n\nContent: {statute_content}"
    else:
        return f"{generated_response}\n\n{statute_content}"  # In case of scraper failure

