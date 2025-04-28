import asyncio
import sys
from tmdb_client import TMDBClient
from openai import OpenAI
from embedding_pipeline import embed_and_format
from vectorstore_pipeline import connect_qdrant, create_qdrant_collection, batch_insert_into_qdrant
from config import TMDB_API_KEY, QDRANT_API_KEY, QDRANT_ENDPOINT, OPENAI_API_KEY, QDRANT_MOVIE_COLLECTION_NAME, QDRANT_TV_COLLECTION_NAME

# Set compatible event loop if running on Windows to avoid shutdown errors
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

MOVIES_COUNT_IN_K = 10  # Number of movies to fetch in thousands
TV_SHOWS_COUNT_IN_K = 10  # Number of TV shows to fetch in thousands
MIN_RATING = 7.0  # Minimum rating for movies to be included
MAX_CONNECTIONS = 15
TIMEOUT = 10
VECTOR_SIZE = 1536  # Size of the vector based on each embedding model

async def main():
    tmdb_client = TMDBClient(api_key=TMDB_API_KEY, max_connections=MAX_CONNECTIONS, timeout=TIMEOUT)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    qdrant_client = connect_qdrant(api_key=QDRANT_API_KEY, endpoint=QDRANT_ENDPOINT)

    try:
        media_ids = await tmdb_client.fetch_media_ids_bulk(
            media_type="tv", 
            media_count_in_k=TV_SHOWS_COUNT_IN_K, 
            rating=MIN_RATING
        )

        media_details = await tmdb_client.fetch_all_media_details(
            media_type="tv", 
            media_ids=media_ids
        )

        formatted_media_with_embedding = await embed_and_format(
            media_type="tv",
            media_details=media_details,
            openai_client=openai_client
        )

        create_qdrant_collection(qdrant_client, QDRANT_TV_COLLECTION_NAME, VECTOR_SIZE)
        batch_insert_into_qdrant(qdrant_client, QDRANT_TV_COLLECTION_NAME, formatted_media_with_embedding)

    finally:
        await tmdb_client.aclose()
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())