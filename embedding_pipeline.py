import asyncio
from typing import Dict, Tuple
from datetime import datetime
from openai import OpenAI


def format_movie_text(movie: Dict) -> Tuple[str, Dict]:
    movie_id = movie.get("id", 0)
    title = movie.get("title", "Unknown Title")
    genre_list = [genre["name"] for genre in movie.get("genres", [])]
    overview = movie.get("overview", "No overview available.")
    tagline = movie.get("tagline", "")
    director = movie.get("director", "Unknown")
    star_list = movie.get("stars", [])
    keyword_list = movie.get("keywords", [])
    provider_list = movie.get("providers", [])
    collection = movie.get("belongs_to_collection", {}).get("name", "") if movie.get("belongs_to_collection") else ""
    poster_path = movie.get("poster_path", "")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
    popularity = movie.get("popularity", 0)
    vote_average = movie.get("vote_average", 0)
    vote_count = movie.get("vote_count", 0)

    try:
        release_date = datetime.strptime(movie.get("release_date", ""), "%Y-%m-%d").replace(hour=0, minute=0, second=0).isoformat() + "Z"
    except ValueError:
        release_date = None

    content = f"""
    Title: {title}
    Genres: {", ".join(genre_list)}
    Overview: {overview}
    Tagline: {tagline}
    Director: {director}
    Stars: {", ".join(star_list)}
    Release Date: {release_date[:10]}
    Keywords: {", ".join(keyword_list)}
    Collection: {collection}
    Poster URL: {poster_url}
    """

    metadata = {
        "movie_id": movie_id,
        "title": title,
        "genres": genre_list,
        "overview": overview,
        "director": director,
        "stars": star_list,
        "release_date": release_date,
        "keywords": keyword_list,
        "collection": collection,
        "watch_providers": provider_list,
        "poster_url": poster_url,
        "popularity": popularity,
        "vote_average": vote_average,
        "vote_count": vote_count,
        "content": content.strip()  
    }

    return content.strip(), metadata

async def embed_text(client: OpenAI, text: str) -> list:
    return await asyncio.to_thread(
        lambda: client.embeddings.create(input=text, model="text-embedding-3-small").data[0].embedding
    )

async def process_movies(movie_details, openai_client):
    formatted_movies = []
    tasks = []
    
    print (f"Formatting and embedding movie data.")
    for content, metadata in map(format_movie_text, movie_details):
        tasks.append(embed_text(client=openai_client, text=content))
    
    embeddings = await asyncio.gather(*tasks)
    
    for (content, metadata), embedding in zip(map(format_movie_text, movie_details), embeddings):
        formatted_movies.append({
            "content": content,
            "embedding": embedding,
            "metadata": metadata
        })
    
    return formatted_movies