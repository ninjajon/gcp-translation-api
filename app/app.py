import streamlit as st
from utils import route_input
import random

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
    st.title("Trainslator v0.5")
    st.markdown("Trainslator is a corporate, private and secure translator")
    st.write("\n")
    st.markdown("""
    Release Notes:
     - Version 0.1 - Translate text from typed input (EN to FR)
     - Version 0.2 - Translate PDF documents (EN to FR)  
     - Version 0.3 - Make UI nicer     
     - Version 0.4 - Add glossary option 
     - Version 0.5 - Improve glossary look 
     - Version 0.6 - FR to EN translation
                """)
    st.markdown("Built with Google Cloud Translate API")
    st.markdown("Source Code: https://github.com/ninjajon/gcp-translation-api")

top_container = st.container(height=400, border=False)
top_container.markdown("<h1 style='text-align: left; font-size: 5em;'>Trainslator</h1>", unsafe_allow_html=True)

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
    source_language_code = "en"
    target_language_code = "fr"
    input_column, middle_column, output_column = st.columns([0.45, 0.1, 0.45], gap="small", vertical_alignment="top")

    input_container_css = '''
    <style>
        div.stFileUploaderFile.st-emotion-cache-12xsiil.e1b2p2ww5 {
            background-color: rgb(240, 242, 246);
        }
        [data-testid='stFileUploader'] {
            width: max-content;
        }
        [data-testid='stFileUploader'] section {
            padding: 0;
            float: left;
        }
        [data-testid='stFileUploader'] section > input + div {
            display: none;
        }
        [data-testid='stFileUploader'] section + div {
            float: right;
            padding-top: 0;
        }
        [data-testid='stFileUploader'] section + div {
            background-color: rgb(240, 242, 246);
            border-radius: 10px; /* Adjust the value to control the roundness */
        }
        [data-testid="stWidgetLabel"] {
            display: none !important;
        }
        div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] {
            background-color: #f0f0f0; 
            padding-left: 5px; /* Add left padding */
            padding-right: 5px; /* Add right padding */
        }
    </style>
    '''

    with input_column:
        input_language = st.selectbox("input_language",("English", "French"))
        input_container = st.container(border=False)
        text_input = input_container.text_area(".", placeholder="Type or your text here or upload a file")
        uploaded_file = input_container.file_uploader(".", type=["pdf","docx", "pptx"], help=None)
        input_container.markdown(input_container_css, unsafe_allow_html=True)

    with middle_column:
        button_pressed = ""
        use_glossary = False
        if st.button("Translate", type="secondary"):
            button_pressed = True
        if st.button("Trainslate", type="primary"):
            use_glossary = True
            button_pressed = True
        st.link_button("See Glossary", "glossary")

    with output_column:
        if input_language == "English":
            output_language = st.selectbox("output_language",("French", "English"), disabled=True)
            source_language_code = "en"
            target_language_code = "fr"
        else:
            output_language = st.selectbox("output_language",("English", "French"), disabled=True)
            source_language_code = "fr"
            target_language_code = "en"
        output_container = st.container(border=False)
        if button_pressed:
            if text_input == "" and uploaded_file is None:
                output_container.write("Please type text to be translated or upload a file")
            else:
                with st.spinner("Trainslating..."):
                    request_id = str(random.randint(100000, 999999))
                    output = route_input(
                        request_id, 
                        text_input, 
                        uploaded_file, 
                        source_language_code, 
                        target_language_code,
                        st.secrets["project_id"], 
                        st.secrets["location"],
                        use_glossary
                    )
                    if uploaded_file is not None:
                        # Store the translated document in a temporary file
                        with open('/tmp/output.pdf', 'wb') as f:
                            f.write(output)

                        # Streamlit download button
                        with open('/tmp/output.pdf', 'rb') as f:
                            output_container.download_button(
                                label="Download Translated File",
                                data=f,
                                file_name="translated_document.pdf",
                                mime="application/pdf"
                            )
                    else:
                        output_container.text_area(".", output)