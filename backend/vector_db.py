import chromadb

client = chromadb.PersistentClient(path=".chromadb")

vector_collection = client.get_or_create_collection(
    name="wuwa_knowledge_base",
    metadata={"hnsw:space": "cosine"}
)


def add_document(id: str, text: str, metadata: dict):
    vector_collection.add(
        documents=[text],
        ids=[id],
        metadatas=[metadata]
    )


def query_docs(query: str, n=3):
    results = vector_collection.query(
        query_texts=[query],
        n_results=n
    )
    return results["documents"][0]
