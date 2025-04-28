import asyncio
from typing import Dict, Tuple, List
from datetime import datetime
from openai import OpenAI


def format_media_text(media_type: str, media: Dict) -> Tuple[str, Dict]:
    # Common fields with type-specific fallbacks
    media_id = media.get("id", 0)
    title = media.get("title" if media_type == "movie" else "name", "Unknown")
    genre_list = [genre["name"] for genre in media.get("genres", [])]
    overview = media.get("overview", "No overview available.")
    tagline = media.get("tagline", "")
    star_list = media.get("stars", [])
    keyword_list = media.get("keywords", [])
    provider_list = media.get("providers", [])
    popularity = media.get("popularity", 0)
    vote_average = media.get("vote_average", 0)
    vote_count = media.get("vote_count", 0)
    poster_path = media.get("poster_path", "")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""    
    
    # Handle release date differently based on media type
    date_field = "release_date" if media_type == "movie" else "first_air_date"
    try:
        dt = datetime.strptime(media.get(date_field, ""), "%Y-%m-%d")
        release_date = dt.replace(hour=0, minute=0, second=0).isoformat() + "Z"
        release_year = dt.year
    except ValueError:
        release_date = release_year = formatted_date = None

    # Media type specific fields
    if media_type == "movie":
        director = media.get("director", "Unknown")
        collection = media.get("belongs_to_collection", {}).get("name", "") if media.get("belongs_to_collection") else ""
        specific_fields = {
            "director": director,
            "collection": collection,
        }
        specific_content = f"Director: {director}"
    else:  # TV show
        creator = media.get("creator", [])
        creator_text = ", ".join(creator) if isinstance(creator, list) else creator
        season_count = media.get('number_of_seasons', None)
        specific_fields = {
            "creator": creator,
            "season_count": season_count,
        }
        specific_content = f"Number of Seasons: {season_count}\nCreator: {creator_text}"

    # Build content string with conditional parts
    content = f"""
    Title: {title}
    Genres: {", ".join(genre_list)}
    Overview: {overview}
    Tagline: {tagline}
    {specific_content}
    Stars: {", ".join(star_list)}
    Release Date: {release_date[:10]}
    Keywords: {", ".join(keyword_list)}
    Poster URL: {poster_url}
    """.strip()
    
    # Build metadata dictionary
    metadata = {
        "media_id": media_id,
        "media_type": media_type,
        "title": title,
        "genres": genre_list,
        "overview": overview,
        "stars": star_list,
        "release_date": release_date,
        "release_year": release_year,
        "keywords": keyword_list,
        "watch_providers": provider_list,
        "poster_url": poster_url,
        "popularity": popularity,
        "vote_average": vote_average,
        "vote_count": vote_count,
        "content": content  # Text to be embedded and retrieved
    }
    
    # Add media-specific fields to metadata
    metadata.update(specific_fields)
    
    return content, metadata


async def embed_text(client: OpenAI, text: str) -> list:
    return await asyncio.to_thread(
        lambda: client.embeddings.create(input=text, model="text-embedding-3-small").data[0].embedding
    )


async def embed_and_format(media_type: str, media_details: List[dict], openai_client: OpenAI) -> List[dict]:
    formatted_media = []
    embed_tasks = []
    formatted_pairs = []

    print(f"✨ Formatting and embedding {len(media_details)} {media_type.upper()} items...")

    for media in media_details:
        content, metadata = format_media_text(media_type, media)
        formatted_pairs.append((content, metadata))
        embed_tasks.append(embed_text(client=openai_client, text=content))

    embeddings = await asyncio.gather(*embed_tasks)

    for (content, metadata), embedding in zip(formatted_pairs, embeddings):
        formatted_media.append({
            "content": content,
            "embedding": embedding,
            "metadata": metadata
        })

    return formatted_media