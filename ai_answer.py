import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"


def build_context(topics):
    blocks = []
    for t in topics:
        text = f"""
TOPIC: {t.title}

SUMMARY:
{t.short_description}

DETAILS:
{t.details}
"""
        blocks.append(text.strip())
    return "\n\n---\n\n".join(blocks)


def generate_answer(question: str, topics):
    context = build_context(topics)

    prompt = f"""
    You are a friendly and practical AI helper for first-year students at Metropolia University of Applied Sciences.

    Your job:
    - Answer clearly and helpfully using the information in CONTEXT.
    - Rephrase and summarize naturally – do NOT talk about the context or what it does or does not contain.
    - Give direct advice to the student.
    - Be concise and supportive.
    - If the answer is not available at all, say:
      "I'm not fully sure based on the available info, but here's what I'd suggest…"

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print("LLM ERROR:", e)
        return None
