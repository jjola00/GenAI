# responses.py

def format_response(answer, citations=None):
    formatted_answer = answer
    if citations:
        formatted_answer += "\n\nCitations:\n" + "\n".join(citations)
    return formatted_answer

