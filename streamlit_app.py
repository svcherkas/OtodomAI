import streamlit as st
from st_functions import st_button, load_css
from PIL import Image

load_css()

st.write("[![Star](https://img.shields.io/github/stars/dataprofessor/links.svg?logo=github&style=social)](https://gitHub.com/dataprofessor/links)")

col1, col2, col3 = st.columns(3)
col2.image(Image.open('dp.png'))

st.header('OtodomAI')

st.info('OtodomAI')

icon_size = 20

st_button('OtodomAI', 'https://www.otodom.pl/', 'OtodomAI', icon_size)

