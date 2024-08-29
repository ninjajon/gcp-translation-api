from google.cloud import translate_v3 as translate

glossary_id = "projects/589130920841/locations/us-central1/glossaries/trainslator-glossary"

def delete_glossary(glossary_id):
    # Create a client
    client = translate.TranslationServiceClient()

    # Initialize request argument(s)
    request = translate.DeleteGlossaryRequest(
        name=glossary_id,
    )

    # Make the request
    operation = client.delete_glossary(request=request)

    print("Deleting glossary...")

    response = operation.result()

    # Handle the response
    print(response)

delete_glossary(glossary_id)