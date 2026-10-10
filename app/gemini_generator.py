from .config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text

def generate_workout_gemini(name, age, weight, goal, intensity):
    prompt = f"""
You are FitBuddy, a careful fitness-planning assistant.
Create a practical 7-day beginner-friendly fitness plan for:
Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}

Return exactly these sections:
DAY 1 through DAY 7.
For every day include:
- Focus
- Warm-up (5-10 minutes)
- Main workout (exercise, sets/reps or duration, rest)
- Cool-down/recovery

Use sensible progression and include rest/recovery days where appropriate.
Do not prescribe extreme dieting, dangerous exercise, or medical treatment.
Add a short "Safety note" telling the user to stop if they feel pain or unwell and to seek professional guidance for medical conditions.
"""
    return generate_text(prompt, GEMINI_WORKOUT_MODEL)
