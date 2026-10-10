from functools import lru_cache
from google import genai
from .config import GOOGLE_API_KEY

@lru_cache(maxsize=1)
def get_client():
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is missing. Add it to your .env file.")
    return genai.Client(api_key=GOOGLE_API_KEY)

def generate_text(prompt: str, model: str) -> str:
    response = get_client().models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
