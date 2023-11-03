import streamlit as st
import torch
import pandas as pd

frame = []
for api in dir(torch):
    frame.append([api])

df = pd.DataFrame(frame, columns=("API Name",))

st.set_page_config(page_title="PyTorch API", page_icon="📚")

st.markdown("# PyTorch API Reference")

st.dataframe(df)


