from .config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text

def update_workout_plan(original_plan, feedback, goal, intensity):
    prompt = f"""
You are FitBuddy updating an existing 7-day fitness plan.
Fitness goal: {goal}
Intensity: {intensity}

Original plan:
{original_plan}

User feedback:
{feedback}

Create a revised 7-day plan that responds directly to the feedback while remaining realistic and safe.
Keep the same clear DAY 1 to DAY 7 structure, with focus, warm-up, main workout, and cool-down/recovery.
Do not include extreme exercise, unsafe instructions, or medical treatment.
Finish with a short safety note.
"""
    return generate_text(prompt, GEMINI_WORKOUT_MODEL)
