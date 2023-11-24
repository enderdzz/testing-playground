__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import plotly.express as px
import chromadb
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="../embedding-db")
collection = chroma_client.get_collection(name="torch.nn")
# collection.add(
#         embeddings=[[1.0, 0.1],],
#         documents=["A person",],
#         metadatas=[{"source": "test"},],
#         ids=["id1",]
# )
emb_list = collection.get(
    include=['embeddings'],
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
)['embeddings']
api_list = collection.get(
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
)['ids']
# for i in emb_list:
#     ans = collection.query(
#         query_embeddings=[i],
#         # include=['embeddings'],
#         n_results=10,
#         # where={"metadata_field": "is_equal_to_this"},
#         # where_document={"$contains":"search_string"}
#     )
#     print(ans['ids'], ans['distances'])

emb = np.array(emb_list)
#print(collection.get(ids=['id2'], include=['embeddings'])['embeddings'])
print(emb.shape)

def visualize_3d(embs, api_list):
    pca = PCA(n_components=3)
    vis_dims = pca.fit_transform(embs)
    sub_matrix = np.array(vis_dims.tolist())
    kmeans_model = KMeans(n_clusters=20, n_init=10) # from 8 to 20
    kmeans_model.fit(sub_matrix)
    cluster_list = kmeans_model.labels_
    
    df = pd.DataFrame({'x': sub_matrix[:, 0],
                       'y': sub_matrix[:, 1],
                       'z': sub_matrix[:, 2],
                       'api_name': api_list,
                       'cluster': cluster_list,
                       })
    
    fig = px.scatter_3d(df, x='x', y='y', z='z', color='cluster', hover_name='api_name')
    #fig = px.scatter_3d(df, x='x', y='y', z='z', mode='markers+text', , color='cluster')
    fig.update_layout(width=900, height=900)
    fig.update_traces(textposition='middle center')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    def set_bgcolor(bg_color = "rgb(211, 211, 211)",
                grid_color="rgb(150, 150, 150)", 
                zeroline=False):
        return dict(showbackground=True,
                backgroundcolor=bg_color,
                gridcolor=grid_color,
                zeroline=zeroline)
    fig.update_scenes(xaxis=set_bgcolor(), 
                  yaxis=set_bgcolor(), 
                  zaxis=set_bgcolor())
    fig.show()

visualize_3d(emb, api_list)