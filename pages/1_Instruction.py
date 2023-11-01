import streamlit as st

st.set_page_config(page_title="Target Installation Instructions", page_icon="📚")

st.markdown("# Target Installation Instructions")

st.write(
"""

Python==3.10.x

### TensorFlow (2.16.0)
----------
```
pip install tf-nightly-cpu==2.16.0.dev20231101
```

### PyTorch (2.2.0)
----------
```
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

### TVM (0.15.dev0)
----------
Build from source
"""
)