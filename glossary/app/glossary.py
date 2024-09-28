import streamlit as st
from utils import route_input
import random
from st_files_connection import FilesConnection
import logging

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Trainslator",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get help": "https://github.com/ninjajon/gcp-translation-api",
        "About": """
            ## Trainslator
            **GitHub**: https://github.com/ninjajon/gcp-translation-api
        """
    }
)

with st.sidebar:
    st.title("Trainslator Glossary v0.1")
    st.markdown("Trainslator is a corporate, private and secure translator")
    st.write("\n")
    st.markdown("""
    Release Notes:
     - Version 0.1 - Show list of entries in Glossary
                """)
    st.markdown("Built with Google Cloud Translate API")
    st.markdown("Source Code: https://github.com/ninjajon/gcp-translation-api")

top_container = st.container(height=400, border=False)
top_container.markdown("<h1 style='text-align: left; font-size: 5em;'>Trainslator Glossary</h1>", unsafe_allow_html=True)

# Set the background image
top_container_css = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://www.cn.ca/-/media/images/stories/2024/ainr-940x400.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
header[data-testid="stHeader"] {
  background-color: transparent !important; 
  opacity: 0.5; /* Adjust this value as needed */
  color: black;
}
</style>
"""

top_container.markdown(top_container_css, unsafe_allow_html=True)

bottom_container = st.container()
with bottom_container:
    st.markdown("Glossary")
    file_uri = st.secrets["file_uri"]
    conn = st.connection('gcs', type=FilesConnection)
    df = conn.read(file_uri, input_format="csv", ttl=600)
    logging.info(df)
    st.dataframe(df.style.highlight_max(axis=0))
    #for row in df.itertuples():
     #   st.write(f"{row.en} has a :{row.fr}:")
