from google.cloud import translate_v3 as translate
from google.cloud import storage

def create_bucket(bucket_name):
    try:
        storage_client = storage.Client()
        storage_client.create_bucket(bucket_name)
    except:
        print(f"Bucket {bucket_name} already exists.")

def upload_glossary(bucket_name, folder_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(f"{folder_name}/{file_name}")
    blob.upload_from_filename(file_name)

def create_glossary(
    project_id: str = "YOUR_PROJECT_ID",
    input_uri: str = "YOUR_INPUT_URI",
    glossary_id: str = "YOUR_GLOSSARY_ID",
    timeout: int = 180,
) -> translate.Glossary:
    """
    Create a equivalent term sets glossary. Glossary can be words or
    short phrases (usually fewer than five words).
    https://cloud.google.com/translate/docs/advanced/glossary#format-glossary
    """
    client = translate.TranslationServiceClient()

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    source_lang_code = "en"
    target_lang_code = "fr"
    location = "us-central1"  # The location of the glossary

    name = client.glossary_path(project_id, location, glossary_id)
    language_codes_set = translate.types.Glossary.LanguageCodesSet(
        language_codes=[source_lang_code, target_lang_code]
    )

    gcs_source = translate.types.GcsSource(input_uri=input_uri)

    input_config = translate.types.GlossaryInputConfig(gcs_source=gcs_source)

    glossary = translate.types.Glossary(
        name=name, language_codes_set=language_codes_set, input_config=input_config
    )

    parent = f"projects/{project_id}/locations/{location}"
    # glossary is a custom dictionary Translation API uses
    # to translate the domain-specific terminology.
    operation = client.create_glossary(parent=parent, glossary=glossary)

    result = operation.result(timeout)
    print(f"Created: {result.name}")
    print(f"Input Uri: {result.input_config.gcs_source.input_uri}")

    return result


