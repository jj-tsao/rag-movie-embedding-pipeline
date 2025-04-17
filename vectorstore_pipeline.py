import qdrant_client
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.http.models import VectorParams, Distance
from tqdm import tqdm


def connect_qdrant(api_key: str, endpoint: str) -> qdrant_client.QdrantClient:
    try:
        client = QdrantClient(
            url=endpoint,
            api_key=api_key
        )
        print ("✅ Connected to Qdrant.")
        return client
    except Exception as e:
        print(f"❌ Error connecting to Qdrant: {e}")
        raise


def create_qdrant_collection(client: qdrant_client, collection_name: str, vector_size: int):
    try:
        if collection_name in [c.name for c in client.get_collections().collections]:
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


def batch_insert_into_qdrant(client, collection_name, data, batch_size=100):
    for i in tqdm(range(0, len(data), batch_size), desc="📤 Inserting batches"):
        batch = data[i:i+batch_size]
        try:
            points = [
                PointStruct(
                    id=item["metadata"]["movie_id"],
                    vector=item["embedding"],
                    payload=item["metadata"]
                )
                for item in batch
            ]
            client.upload_points(
                collection_name=collection_name,
                points=points,
                wait=True
            )
            print(f"✅ Inserting batch {i // batch_size + 1} with {len(points)} points.")
        except Exception as e:
            print(f"❌ Error inserting batch {i // batch_size + 1} into Qdrant: {e}")
