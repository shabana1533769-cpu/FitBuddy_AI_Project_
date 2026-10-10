import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")
GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-flash")
GEMINI_TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-2.5-flash")
