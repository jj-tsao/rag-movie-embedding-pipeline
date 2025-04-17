import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_ENDPOINT = os.getenv("QDRANT_ENDPOINT")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

if not OPENAI_API_KEY or not TMDB_API_KEY or not QDRANT_API_KEY:
    raise EnvironmentError("Missing required API key(s)")
if not QDRANT_ENDPOINT or not QDRANT_COLLECTION_NAME:
    raise EnvironmentError("QDrant URL or collection name is not set.")