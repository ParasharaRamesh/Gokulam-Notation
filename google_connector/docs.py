# Contains apis related to google docs

def get_document(client, docId):
    '''
    Gets a document given docId

    :param client:
    :param docId:
    :return:
    '''
    return client.documents().get(documentId=docId).execute()

def insert_text_into_document(client, docId, text, index):
    '''
    Inserts the text into a given document with docId at the location index

    :param client:
    :param docId:
    :param text:
    :param index:
    :return:
    '''
    requests = [{
        "insertText": {
            "location": {
                "index": index,
            },
            "text": text
        }
    }]
    result = client.documents().batchUpdate(documentId = docId, body = {"requests": requests}).execute()
    return result