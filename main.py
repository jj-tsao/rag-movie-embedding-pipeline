import asyncio
import sys
from tmdb_client import TMDBClient
from embedding_pipeline import process_movies
from openai import OpenAI
from vectorstore_pipeline import connect_qdrant, create_qdrant_collection, batch_insert_into_qdrant
from config import TMDB_API_KEY, QDRANT_API_KEY, QDRANT_ENDPOINT, QDRANT_COLLECTION_NAME, OPENAI_API_KEY

# Set compatible event loop if running on Windows to avoid shutdown errors
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

MOVIES_COUNT_IN_K = 10  # Number of movies to fetch in thousands
RATING = 6.0  # Minimum rating for movies to be included
MAX_CONNECTIONS = 15
TIMEOUT = 10
VECTOR_SIZE = 1536  # Size of the vector based on your embedding model

async def main():
    tmdb_client = TMDBClient(api_key=TMDB_API_KEY, max_connections=MAX_CONNECTIONS, timeout=TIMEOUT)
    qdrant_client = connect_qdrant(api_key=QDRANT_API_KEY, endpoint=QDRANT_ENDPOINT)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        movie_ids = await tmdb_client.fetch_movie_ids_bulk(movies_count_in_k=MOVIES_COUNT_IN_K, rating=RATING)
        movie_details = await tmdb_client.fetch_all_movie_details(movie_ids)

        formatted_movies_with_embedding = await process_movies(movie_details, openai_client)
        create_qdrant_collection(qdrant_client, QDRANT_COLLECTION_NAME, VECTOR_SIZE)
        batch_insert_into_qdrant(qdrant_client, QDRANT_COLLECTION_NAME, formatted_movies_with_embedding, VECTOR_SIZE)

    finally:
        await tmdb_client.aclose() 
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())