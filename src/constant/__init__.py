import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ARTIFACT_DIR = "artifacts"
LOG_DIR = "logs"
