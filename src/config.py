import os
from dotenv import load_dotenv

load_dotenv()

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in .env")

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# REST Countries API
COUNTRIES_API_BASE = "https://restcountries.com/v3.1"
