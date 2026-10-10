from .config import GEMINI_TIP_MODEL
from .gemini_client import generate_text

def generate_nutrition_tip_with_flash(goal):
    prompt = f"""
Give one concise, practical nutrition or recovery tip for a person whose fitness goal is "{goal}".
Keep it general and healthy. Avoid calorie prescriptions, extreme restriction, supplements, or medical claims.
Return 2-4 sentences maximum.
"""
    return generate_text(prompt, GEMINI_TIP_MODEL)
