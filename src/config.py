import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHUNK_SIZE = 400
CHUNK_OVERLAP = 40

TOP_K = 3

CONFIDENCE_THRESHOLD = 0.4