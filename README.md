# 🎥 RAG Movie Data Embedding Pipeline 

A modular Python pipeline that fetches movie and TV show metadata from TMDB, embeds it using fine-tuned SentenceTransformers model, and uploads it to Qdrant Cloud for use in a semantic/hybrid RAG system.

---

## 🔗 Related Project

👉 Frontend app: [RAG Movie Recommender](https://github.com/jj-tsao/rag-movie-recommender-app)  
👉 Live demo: [Hugging Face Spaces](https://huggingface.co/spaces/JJTsao/RAG_Movie_Recommendation_Assistant)
👉 Moedel Training Data Pipeline: [[rag-movie-training-pipeline]](https://github.com/jj-tsao/rag-movie-training-pipeline)

---

## 🧬 Pipeline Overview

- 🎬 **Fetch**: Pulls metadata from TMDB (titles, genres, cast, plot, streaming, keywords, etc.)
- 🧠 **Embed**: Encodes media content using fine-tuned `bge-base-en-v1.5` SentenceTransformer
- 🧹 **Format**: Structures rich metadata + natural text for hybrid search
- ☁️ **Upload**: Inserts vectors + payloads into Qdrant with optional retries
- ⚡ **Async & Batched**: Uses `httpx.AsyncClient` and smart batching for efficient API throughput

---

## 🔧 Tech Stack

- Python 3.10+
- [TMDB API](https://developer.themoviedb.org/)
- [Qdrant](https://qdrant.tech/)
- [OpenAI](https://platform.openai.com/)
- [SentenceTransformers](https://www.sbert.net/)
- [HTTPX](https://www.python-httpx.org/)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/jj-tsao/rag-movie-embedding-pipeline.git
cd rag-movie-embedding-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file:
```
TMDB_API_KEY=your_tmdb_key
OPENAI_API_KEY=your_openai_key
QDRANT_API_KEY=your_qdrant_key
QDRANT_ENPOINT=https://your-qdrant-endpoint-url
QDRANT_MOVIE_COLLECTION_NAME=your_qdrant_movie_collection_name
QDRANT_TV_COLLECTION_NAME=your_qdrant_tv_collection_name
```

### 4. Run the pipeline

```bash
python main.py
```

---

## 📂 Folder Structure

```
├── main.py                 # Main entry point
├── tmdb_client.py          # TMDB async fetcher
├── embedding_pipeline.py   # Embeds & formats media content
├── vectorstore_pipeline.py # Creates Qdrant collection, uploads vectors
├── config.py               # Env vars and constants
└── requirements.txt        # Python dependencies
```

---

## 🔁 Reusability

The pipeline is modular and reusable for:
- Other content domains (e.g. books, podcasts, news)
- Other vector DBs (e.g. ChromaDB, Weaviate, Pinecone)
- Other embedding models (e.g. HuggingFace, Cohere, etc.)

---

## 📄 License

[MIT License](LICENSE)
