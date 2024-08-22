import os
import json
from google.cloud import translate
from google.cloud import translate_v3
import logging

logging.basicConfig(level=logging.INFO)

def route_input(request_id, text_input, uploaded_file, source_language_code, target_language_code, project_id, location):
    logging.info(f"{request_id} - Request ID: {request_id}")
    logging.info(f"{request_id} - New Input: {text_input}")
    if uploaded_file is not None:
        logging.info(f"{request_id} - Uploaded File Type: {uploaded_file.type}")
        output = translate_file(request_id, uploaded_file, source_language_code, target_language_code, project_id, location)
    else:
        logging.info(f"{request_id} - No Uploaded File")
        output = translate_text(request_id, text_input, source_language_code, target_language_code, project_id, location)
    return output

def translate_text(request_id, text_input, source_language_code, target_language_code, project_id, location
    ) -> translate.TranslationServiceClient:

    logging.info(f"{request_id} - Sending text input to Cloud Translate API...")

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent= parent,
        contents= [text_input],
        mime_type= "text/plain",  # mime types: text/plain, text/html
        source_language_code= source_language_code,
        target_language_code= target_language_code
    )

    translated_text = response.translations[0].translated_text
    logging.info(f"{request_id} - Translated Text: {translated_text}")

    return translated_text

def translate_file(request_id, uploaded_file, source_language_code, target_language_code, project_id, location
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

    response = client.translate_document(
        request={
            "parent": parent,
            "target_language_code": "fr",
            "document_input_config": document_input_config,
        }
    )

    # f = open('/tmp/output', 'wb')
    # f.write(response.document_translation.byte_stream_outputs[0])
    # f.close()

    return response.document_translation.byte_stream_outputs[0]


    # try:
    #     if uploaded_file.type in ("image/png", "image/jpeg"):
    #         bytes_data = uploaded_file.getvalue()
    #         file_content = Image.from_bytes(bytes_data)
    #     elif uploaded_file.type in ("application/pdf"):
    #         bytes_data = uploaded_file.getvalue()
    #         file_content = Part.from_data(mime_type="application/pdf", data=bytes_data)
    #     else:
    #         logging.warning(f"{request_id} - Unknown file type")
    # except:
    #     logging.warning(f"{request_id} - Can't read file")

    #     return "Can't read the uploaded file. Try with a different one."

    # system_instruction = set_system_instruction(persona, "file")

    # logging.info(f"{request_id} - Sending prompt to Gemini...")
    # model = GenerativeModel(
    #     model_name=model_id,
    #     system_instruction=[system_instruction]
    # )
    # generation_config = {
    #     "max_output_tokens": 8192,
    #     "temperature": temperature,
    #     "top_p": 0.95,
    # }

    # response = model.generate_content(
    #     [file_content, question],
    #     generation_config=generation_config
    # )
    # answer = response.text

    # logging.info(f"{request_id} - Response from Gemini is: {answer}")

    # return answer
