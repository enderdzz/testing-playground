import chromadb
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="../embedding-db")
collection = chroma_client.get_or_create_collection(name="torch_api")
# collection.add(
#         embeddings=[[1.0, 0.1],],
#         documents=["A person",],
#         metadatas=[{"source": "test"},],
#         ids=["id1",]
# )
ans = collection.get(
    include=['embeddings'],
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
)['embeddings']
print(len(ans))
emb = np.array(ans)
#print(collection.get(ids=['id2'], include=['embeddings'])['embeddings'])
print(emb.shape)
def visualize_3d(embedding):
    pca = PCA(n_components=3)
    vis_dims = pca.fit_transform(embedding)

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(projection='3d')
    cmap = plt.get_cmap("tab20")
    
    sub_matrix = np.array(vis_dims.tolist())
    x=sub_matrix[:, 0]
    y=sub_matrix[:, 1]
    z=sub_matrix[:, 2]
    colors = [cmap(1)] * len(sub_matrix)
    ax.scatter(x, y, zs=z, zdir='z', c=colors, label='API')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend(bbox_to_anchor=(1.1, 1))
    
    fig.savefig("vis3d.png")

visualize_3d(emb)