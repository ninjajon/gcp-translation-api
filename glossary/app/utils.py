from google.cloud import translate
import logging
import streamlit as st

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
    if uploaded_file.type not in ("application/pdf"):
        return "Your file type is not supported"

    ### read document
    document_content = uploaded_file.read()

    document_input_config = {
        "content": document_content,
        "mime_type": "application/pdf",
    }

    if use_glossary:
        glossary_id = st.secrets["glossary_id"]
        glossary = client.glossary_path(
            project_id, "us-central1", glossary_id  # The location of the glossary
        )
        glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)

    else:
        glossary_config = None

    logging.info(f"{request_id} - Glossary: {glossary_config}")

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
