import chromadb
# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="./test-embedding-db")
collection = chroma_client.get_or_create_collection(name="torch_api")
# collection.add(
#         embeddings=[[1.0, 0.1],],
#         documents=["A person",],
#         metadatas=[{"source": "test"},],
#         ids=["id1",]
# )
ans = collection.query(
    query_embeddings=[[1.1, 0.1]],
    n_results=10,
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
)
print(collection.peek())
print(collection.get(ids=['id2'], include=['embeddings'])['embeddings'])