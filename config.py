import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_ENDPOINT = os.getenv("QDRANT_ENDPOINT")
QDRANT_MOVIE_COLLECTION_NAME = os.getenv("QDRANT_MOVIE_COLLECTION_NAME_MPNET")
QDRANT_TV_COLLECTION_NAME = os.getenv("QDRANT_TV_COLLECTION_NAME_MPNET")
EMBEDDING_MODEL_NAME = "JJTsao/fine-tuned_movie_retriever-all-mpnet-base-v2"  # Fine-tuned sentence transfomer model for movie data embedding 


if not OPENAI_API_KEY or not TMDB_API_KEY or not QDRANT_API_KEY:
    raise EnvironmentError("Missing required API key(s)")
if not QDRANT_ENDPOINT or not QDRANT_MOVIE_COLLECTION_NAME or not QDRANT_TV_COLLECTION_NAME:
    raise EnvironmentError("QDrant URL or collection name is not set.")