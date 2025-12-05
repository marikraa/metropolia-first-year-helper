import os
from groq import Groq

GSK_API_KEY = os.getenv("GSK_API_KEY")

client = None
if GSK_API_KEY:
    client = Groq(api_key=GSK_API_KEY)

MODEL = "llama-3.1-8b-instant"

def build_context(topics):
    blocks = []
    for t in topics:
        blocks.append(
            f"TOPIC: {t.title}\n"
            f"{t.short_description}\n"
            f"{t.details}"
        )
    return "\n\n---\n\n".join(blocks)


def generate_answer(question: str, topics):

    if not client:
        print("GSK_API_KEY missing")
        return None

    prompt = f"""
You are a helpful assistant for first-year students at Metropolia University of Applied Sciences.

Only answer using the information below.
Do not invent details if information is missing.
Write clearly and concisely.

INFORMATION:
{build_context(topics)}

QUESTION:
{question}

ANSWER:
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=150,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ API ERROR:", e)
        return "The AI service is temporarily unavailable."