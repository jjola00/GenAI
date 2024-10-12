# api_client.py

import requests

def get_legal_advice(user_question):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a supportive assistant for individuals seeking legal advice, who presents a sample document which will be sent to lawyer for easier communication."
            },
            {
                "role": "user",
                "content": user_question
            }
        ],
        "max_tokens": 10000,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_citations": True,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }

    headers = {
        "Authorization": "Bearer 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",  # Replace with your actual API key
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

