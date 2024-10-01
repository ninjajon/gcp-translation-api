from google.cloud import translate
import logging
import streamlit as st
from fpdf import FPDF
from google.cloud import storage

logging.basicConfig(level=logging.INFO)

def route_input(request_id, text_input, uploaded_file, source_language_code, target_language_code, project_id, location, use_glossary):
    logging.info(f"{request_id} - Request ID: {request_id}")
    logging.info(f"{request_id} - New Input: {text_input}")
    if uploaded_file is not None:
        logging.info(f"{request_id} - Uploaded File Type: {uploaded_file.type}")
        output = translate_file(request_id, uploaded_file, source_language_code, target_language_code, project_id, location, use_glossary)
    else:
        logging.info(f"{request_id} - No Uploaded File")
        output = translate_text(request_id, text_input, source_language_code, target_language_code, project_id, location, use_glossary)
    return output

def translate_text(request_id, text_input, source_language_code, target_language_code, project_id, location, use_glossary
    ) -> translate.TranslationServiceClient:

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    if use_glossary:
        glossary_id = st.secrets["glossary_id"]
        glossary = client.glossary_path(
            project_id, "us-central1", glossary_id  # The location of the glossary
        )
        glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)
        
    else:
        glossary_config = None

    logging.info(f"{request_id} - Glossary: {glossary_config}")

    logging.info(f"{request_id} - Sending text input to Cloud Translate API...")

    response = client.translate_text(
        request={
            "contents": [text_input],
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "parent": parent,
            "glossary_config": glossary_config,
        }
    )

    if use_glossary:
        translated_text = response.glossary_translations[0].translated_text
        logging.info(f"{request_id} - Glossary Translation: {translated_text}")
    else:     
        translated_text = response.translations[0].translated_text
        logging.info(f"{request_id} - Translation: {translated_text}")
    
    logging.info(f"{request_id} - Translated Text: {translated_text}")

    return translated_text

def translate_file(request_id, uploaded_file, source_language_code, target_language_code, project_id, location, use_glossary
) -> translate.TranslationServiceClient:
    
    client = translate.TranslationServiceClient()
    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    logging.info(f"{request_id} - Transalating uploaded file...")

    ### check file type
    logging.info(f"{request_id} - Uploaded File Type: {uploaded_file.type}")
    logging.info(f"{request_id} - Uploaded File Name: {uploaded_file.name}")

    if use_glossary:
        glossary_id = st.secrets["glossary_id"]
        glossary = client.glossary_path(
            project_id, "us-central1", glossary_id  # The location of the glossary
        )
        glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)

    else:
        glossary_config = None

    logging.info(f"{request_id} - Glossary: {glossary_config}")

    ### read document
    document_content = uploaded_file.read()


    project_id = "jo-vertex-ai-playground-ffyc"
    location = "us-central1"
    bucket_name = "jo-translation-docs"
    input_folder_name = "input"
    input_file_name = "KT_session_with_PwC.vtt"
    converted_folder_name = "converted"
    converted_file_name = "KT_session_with_PwC.pdf"
    output_folder_name = "output"
    output_file_name = "KT_session_with_PwC_FR.pdf"
    source_language_code = "en"
    target_language_code = "fr"


    if uploaded_file.type in ("text/plain", "text/vtt"):
        #upload to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"{converted_folder_name}/{converted_file_name}")
        blob.upload_from_filename(temp_file_path)
        document_content = txt_to_pdf(document_content)
        mime_type = "application/pdf"
    else:
        mime_type = uploaded_file.type

    document_input_config = {
        "content": document_content,
        "mime_type": mime_type
    }

    response = client.translate_document(
        request={
            "parent": parent,
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
            "document_input_config": document_input_config,
            "glossary_config": glossary_config,
        }
    )

    if use_glossary:
        return response.glossary_document_translation.byte_stream_outputs[0]
    else:
        return response.document_translation.byte_stream_outputs[0]

def txt_to_pdf(document_content):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_auto_page_break(auto=True, margin=15)
  pdf.set_font("Arial", size=12)
  
  # Read the text file content
  text_content = document_content.decode("utf-8") 

  print(f"text: {text_content}")

  # Add the text content to the PDF
  pdf.multi_cell(0, 10, text_content)
  
  # Get the PDF output as bytearray
  pdf_output = pdf.output(dest='S') 
  
  # Convert bytearray to bytes
  pdf_bytes = bytes(pdf_output)
  
  return pdf_bytes  # Return the PDF as bytes