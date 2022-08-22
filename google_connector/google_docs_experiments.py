def get_document(client, docId):
    # Retrieve the documents contents from the Docs service.
    return client.documents().get(documentId=docId).execute()

def insert_text_into_document(client, docId, text):
    #inserting headins has to be done!
    requests = [{
        "insertText": {
            "location": {
                "index": 1,
            },
            "text": text
        }
    }]
    #Commenting out so that the pipeline doesnt keep adding stuff!
    result = client.documents().batchUpdate(documentId = docId, body = {"requests": requests}).execute()
    return result

if __name__ == "__main__":
    pass