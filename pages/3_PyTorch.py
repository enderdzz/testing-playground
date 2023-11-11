import streamlit as st
import torch
import pandas as pd
from openai import OpenAI
import inspect
import torch.nn
import tiktoken
import chromadb
#chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="./embedding-db")
collection = chroma_client.get_or_create_collection(name="torch_api")

st.set_page_config(page_title="PyTorch API", page_icon="📚")
st.markdown("# PyTorch API Reference")

def get_api_list(pkg):
    frame = []
    for api in dir(pkg):
        frame.append([api])
    return pd.DataFrame(frame, columns=("API Name",))

st.write("Package: torch")
st.dataframe(get_api_list(torch))

st.write("Package: torch.nn")
st.dataframe(get_api_list(torch.nn))

# Function to retrieve the source code of a given function or class
def get_source_code(api_name):
    try:
        # Import the module and get the attribute (function/class)
        api = eval(api_name)

        # Get the source code
        source_code = inspect.getsource(api)
        return source_code
    except (ImportError, AttributeError):
        return f"API '{api_name}' not found."
    except TypeError:
        return f"Source code for '{api_name}' is not available (might be a built-in or C-extension)."

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

def calculate_embedding(text, model="text-embedding-ada-002"):
    client = OpenAI(api_key=api_key)
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def visualize_2d():
    pass

def visualize_3d():
    pass

api_key  = st.text_input('Enter an OpenAI Key', None)
api_name = st.text_input('Enter an API', 'torch.nn.GRUCell')
source_code = get_source_code(api_name)
st.text_area("Soure Code", value=source_code, height=300, max_chars=None)
st.write(f"There are {num_tokens_from_string(source_code, 'cl100k_base')} tokens.")

def show_embedding():
    embedding = collection.get(ids=[api_name], include=['embeddings'])['embeddings']
    if embedding == []:
        if api_key != None:
            embedding = calculate_embedding(source_code, model='text-embedding-ada-002')
            collection.add(
                embeddings=[embedding,],
                documents=[source_code,],
                metadatas=[{"source": api_name},],
                ids=[api_name,]
            )
        else:
            st.session_state.need_openai_key = True
    if embedding != []:
        st.session_state.embedding = embedding

st.button('Get Embedding!', on_click=show_embedding)
if 'need_openai_key' in st.session_state:
    st.error("Please enter an OpenAI key.")
if 'embedding' in st.session_state:
    st.text_area(f"Output Embedding (Dim: {len(st.session_state.embedding)})", value=st.session_state.embedding, height=300, max_chars=None)


visualize_2d()
visualize_3d()
# ['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
# df.to_csv('output/embedded_1k_reviews.csv', index=False)

