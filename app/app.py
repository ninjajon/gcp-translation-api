import streamlit as st
from utils import route_input
import random

st.set_page_config(
    page_title="Ninja Translate",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get help": "https://github.com/ninjajon/gcp-translation-api",
        "About": """
            ## Ninja Translate
            **GitHub**: https://github.com/ninjajon/gcp-translation-api
        """
    }
)

with st.sidebar:
    st.title("Ninja Translate v0.2")
    st.markdown("Ninja's corporate, private and secure translator")
    st.write("\n")
    st.markdown("""
    Release Notes:
     - Version 0.1 - Translate text from typed input (EN to FR)
     - Version 0.2 - Translate PDF documents (EN to FR)      
                """)
    st.markdown("Built with Google Cloud Translate API")
    st.markdown("Source Code: https://github.com/ninjajon/gcp-translation-api")

st.header("Ninja Translate", divider="rainbow")
st.subheader("Got something to translate?")

text_input = st.text_area("Your text", placeholder="Enter your text here")
uploaded_file = st.file_uploader("Upload your file here (PDF, Word, PowerPoint)", type=["pdf","docx", "pptx"], help=None)
source_language_code = "en"
target_language_code = "fr"

button_pressed = ""
if st.button("Submit", type="secondary"):
    button_pressed = True

if button_pressed:
    if text_input == "" and uploaded_file is None:
        st.write("Please type text to be translated or upload a file")
    else:
        with st.spinner("Translating..."):
            output_container = st.container(border=True)
            request_id = str(random.randint(100000, 999999))
            output = route_input(
                request_id, 
                text_input, 
                uploaded_file, 
                source_language_code, 
                target_language_code,
                st.secrets["project_id"], 
                st.secrets["location"]
            )
            if uploaded_file is not None:
                # Store the translated document in a temporary file
                with open('/tmp/output.pdf', 'wb') as f:
                    f.write(output)

                # Streamlit download button
                with open('/tmp/output.pdf', 'rb') as f:
                    st.download_button(
                        label="Download Translated File",
                        data=f,
                        file_name="translated_document.pdf",
                        mime="application/pdf"
                    )
            else:
                output_container.write(output)