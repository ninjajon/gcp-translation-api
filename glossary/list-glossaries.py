from google.cloud import translate_v3 as translate

def list_glossaries(project_id: str = "jo-trainslator-antl") -> translate.Glossary:
    """List Glossaries.

    Args:
        project_id: The GCP project ID.

    Returns:
        The glossary.
    """
    client = translate.TranslationServiceClient()

    location = "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    glossaries = client.list_glossaries(parent=parent)
    
    if glossaries.glossaries:
        for glossary in glossaries:
            print(f"Name: {glossary.name}")
            print(f"Entry count: {glossary.entry_count}")
            print(f"Input uri: {glossary.input_config.gcs_source.input_uri}")

            for language_code in glossary.language_codes_set.language_codes:
                print(f"Language code: {language_code}")
    else:
        print("No glossaries found.")
        
list_glossaries()