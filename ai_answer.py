import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")

MODEL = "microsoft/Phi-3-mini-4k-instruct"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

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
    # No API key = no AI
    if not HF_API_KEY:
        return None

    context = build_context(topics)

    prompt = f"""
You are a friendly and helpful assistant for first-year students at Metropolia University of Applied Sciences.

Answer using ONLY the provided CONTEXT.
Do not reference the context or discuss rules.
Keep the reply concise and practical.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 180,
            "temperature": 0.2,
            "do_sample": True,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        result = response.json()

        # HF sometimes returns an array, sometimes dict
        if isinstance(result, list):
            return result[0]["generated_text"].strip()

        return result["generated_text"].strip()

    except Exception as e:
        print("HF API ERROR:", e)
        return None
