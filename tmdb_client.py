import asyncio
from typing import Optional, List, Dict
from datetime import date
import httpx
from tqdm import tqdm

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key: str, max_connections: int = 15, timeout: float = 10.0):
        self.api_key = api_key
        limits = httpx.Limits(max_connections=max_connections, max_keepalive_connections=max_connections)
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=limits,
            headers={"Accept": "application/json"}
        )
        self.semaphore = asyncio.Semaphore(max_connections)

    async def get(self, url: str):
        async with self.semaphore:
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"[HTTP Error] {e.response.status_code}: {url}")
            except httpx.RequestError as e:
                print(f"[Request Error] {e}")
            except Exception as e:
                print(f"[Unexpected Error] {e}")
        return None

    async def fetch_movie_ids(
        self,
        page: int = 1,
        genre: Optional[str] = None,
        rating: float = 0,
        vote_count: int = 0
    ) -> List[int]:
        today = date.today()
        url = (
            f"{self.BASE_URL}/discover/movie"
            f"?api_key={self.api_key}&language=en-US&page={page}&region=US"
            f"&primary_release_date.lte={today}&vote_average.gte={rating}&vote_count.gte={vote_count}&sort_by=popularity.desc"
        )
        if genre:
            url += f"&with_genres={genre}"

        data = await self.get(url)
        return [movie["id"] for movie in data.get("results", [])] if data else []

    async def fetch_movie_ids_bulk(
        self,
        movies_count_in_k= 1,
        genre: Optional[str] = None,
        rating: float = 0,
        vote_count: int = 0
    ) -> List[int]:
        total_pages = int(movies_count_in_k * 50)
        print(f"📥 Fetching movie IDs from {total_pages} pages with rating > {rating}...")
        tasks = [
            self.fetch_movie_ids(page, genre, rating, vote_count)
            for page in range(1, total_pages + 1)
        ]
        results = await asyncio.gather(*tasks)
        all_ids = [movie_id for sublist in results if isinstance(sublist, list) for movie_id in sublist]
        print(f"✅ Fetched {len(all_ids):,} movie IDs")
        return all_ids

    async def fetch_movie_details(self, movie_id: int) -> Optional[dict]:
        base = f"{self.BASE_URL}/movie/{movie_id}"
        details_url = f"{base}?api_key={self.api_key}"
        credits_url = f"{base}/credits?api_key={self.api_key}"
        keywords_url = f"{base}/keywords?api_key={self.api_key}"
        providers_url = f"{base}/watch/providers?api_key={self.api_key}"

        movie_details = await self.get(details_url) or {}
        credits_data = await self.get(credits_url)
        keywords_data = await self.get(keywords_url)
        providers_data = await self.get(providers_url)

        if credits_data:
            crew = credits_data.get("crew", [])
            cast = credits_data.get("cast", [])
            movie_details["director"] = next((c["name"] for c in crew if c["job"] == "Director"), "Unknown")
            movie_details["stars"] = [c["name"] for c in cast[:3]] if cast else []
        else:
            movie_details["director"] = "Unknown"
            movie_details["stars"] = []

        if keywords_data:
            movie_details["keywords"] = [kw["name"] for kw in keywords_data.get("keywords", [])]

        if providers_data:
            us_data = providers_data.get("results", {}).get("US", {})
            flatrate = us_data.get("flatrate", [])
            if flatrate:
                movie_details["providers"] = [p["provider_name"] for p in flatrate]

        return movie_details

    async def fetch_all_movie_details(self, movie_ids: List[int]) -> List[dict]:
        tasks = [self.fetch_movie_details(mid) for mid in movie_ids]
        movies = []
        for future in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="🎥 Fetching movie details"):
            try:
                movie = await future
                if movie:
                    movies.append(movie)
            except Exception as e:
                print(f"❌ Error fetching movie details: {e}")
        return movies

    async def aclose(self):
        await self.client.aclose()
