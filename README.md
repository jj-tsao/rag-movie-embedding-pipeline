# 🎥 RAG Movie Data Embedding Pipeline 

A modular Python pipeline to fetch movie data from TMDB, format the content/metadata, embed it using OpenAI, and upload to QDrant Cloud server for use in a RAG-based recommendation system.

---

## 🔗 Related Project

👉 Frontend RAG app: [RAG Movie Recommender](https://github.com/jj-tsao/rag-movie-recommender-app). Check out live demo on [Hugging Face Space](https://huggingface.co/spaces/JJTsao/RAG_Movie_Recommendation_Assistant)

---

## 🧬 What It Does

- 🔄 **Pulls Data** from multiple TMDB APIs (title, overview, rating, release date, credits, streaming options, etc.)
- 🧠 **Embeds Movie Data** using OpenAI's embedding model
- 🧹 **Cleans & Formats** data for vector DB ingestion
- ☁️ **Uploads to QDrant Cloud vectorDB** with hybrid search metadata, ready for runtime access
- 📤 **Asynchronous and Batch Processing** for improved efficiency and compliance with rate limiting

---

## 🔧 Tech Stack

- Python
- TMDB API
- OpenAI Embedding Model
- QDrant Python Client (v1.13.3)
- HTTPX.AsyncClient

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
QDRANT_COLLECTION_NAME=your_qdrant_collection_name
```

### 4. Run the pipeline

```bash
python main.py
```

---

## 📂 Folder Structure

```
├── main.py                 # Entry point to run the full pipeline
├── tmdb_client.py          # Pulls data from TMDB with async HTTP requests
├── embedding_pipeline.py   # Formats and embeds movie data
├── vectorstore_pipeline.py # Uploads data to QDrant Cloud vectorDB
├── config.py               # Configures environment variables
├── .env.example            # Environment variables template
└── requirements.txt        # Python dependencies
```

---

## 🔁 Reusability

The pipeline is modular and reusable for:
- Other domains (e.g. books, podcasts)
- Other vector stores (e.g. ChromaDB, Weaviate)
- Other embedding models (e.g. HuggingFace, Cohere)

---

## 📄 License

[MIT License](LICENSE)