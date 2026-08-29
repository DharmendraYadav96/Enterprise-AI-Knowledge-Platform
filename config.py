import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    QDRANT_PATH = os.getenv(
        "QDRANT_PATH",
        "data/qdrant"
    )