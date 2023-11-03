import streamlit as st
import tvm
import pandas as pd

frame = []
for api in dir(tvm):
    frame.append([api])

df = pd.DataFrame(frame, columns=("API Name",))

st.set_page_config(page_title="TVM API", page_icon="📚")

st.markdown("# TVM API Reference")

st.dataframe(df)


