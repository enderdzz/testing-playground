import streamlit as st
import tensorflow
import pandas as pd

frame = []
for api in dir(tensorflow):
    frame.append([api])

df = pd.DataFrame(frame, columns=("API Name",))

st.set_page_config(page_title="TensorFlow API", page_icon="📚")

st.markdown("# TensorFlow API Reference")

st.dataframe(df)