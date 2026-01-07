import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_project(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior software architect. "
                    "You MUST return ONLY valid JSON. "
                    "Do not include explanations or markdown."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    content = response.choices[0].message.content

    # Force JSON parsing
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise RuntimeError("AI returned invalid JSON")
