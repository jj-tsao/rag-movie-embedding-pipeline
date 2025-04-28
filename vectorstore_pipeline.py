from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from tqdm import tqdm

def connect_qdrant(api_key: str, endpoint: str) -> QdrantClient:
    try:
        client = QdrantClient(
            url=endpoint,
            api_key=api_key,
        )
        print("✅ Connected to Qdrant.")
        return client
    except Exception as e:
        print(f"❌ Error connecting to Qdrant: {e}")
        raise

def create_qdrant_collection(client: QdrantClient, collection_name: str, vector_size: int):
    try:
        collections = client.get_collections().collections
        if collection_name in [c.name for c in collections]:
            print(f"⚠️ Collection '{collection_name}' already exists.")
            return

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )
        print(f"✅ Collection '{collection_name}' created.")
    except Exception as e:
        print(f"❌ Error creating collection: {e}")
        raise

def safe_upload(client, collection_name, points, retries=3):
    import time
    for attempt in range(1, retries + 1):
        try:
            client.upload_points(
                collection_name=collection_name,
                points=points,
                wait=True
            )
            return True
        except Exception as e:
            print(f"⚠️ Upload attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(2 * attempt)
    return False

def batch_insert_into_qdrant(client, collection_name, data, batch_size=100):
    for i in tqdm(range(0, len(data), batch_size), desc="📤 Inserting batches"):
        batch = data[i:i + batch_size]
        try:
            points = [
                PointStruct(
                    id=item["metadata"]["media_id"],
                    vector=item["embedding"],
                    payload=item["metadata"]
                )
                for item in batch
            ]
            success = safe_upload(client, collection_name, points)
            if success:
                print(f"✅ Inserted batch {i // batch_size + 1} with {len(points)} points.")
            else:
                print(f"❌ Failed to insert batch {i // batch_size + 1} after retries.")
        except Exception as e:
            print(f"❌ Error preparing batch {i // batch_size + 1}: {e}")