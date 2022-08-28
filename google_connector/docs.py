# Contains apis related to google docs
import gokulam_notation


def get_document(client, docId):
    '''
    Gets a document given docId

    :param client:
    :param docId:
    :return:
    '''
    try:
        gokulam_notation.app.logger.info(f"Getting document details with docId {docId}")
        return client.documents().get(documentId=docId).execute()
    except Exception as err:
        error = f"Unable to get the document with document id {docId}. Exception is {err}"
        gokulam_notation.app.logger.error(error)
        raise Exception(error)


def insert_text_into_document(client, docId, text, index):
    '''
    Inserts the text into a given document with docId at the location index

    :param client:
    :param docId:
    :param text:
    :param index:
    :return:
    '''
    try:
        requests = [{
            "insertText": {
                "location": {
                    "index": index,
                },
                "text": text
            }
        }]
        gokulam_notation.app.logger.info(
            f"Inserting the text {text} at index {index} in the document with docId {docId} with request body {requests}")
        result = client.documents().batchUpdate(documentId=docId, body={"requests": requests}).execute()
        gokulam_notation.app.logger.info()
        return result
    except Exception as err:
        error = f"Unable to insert text {text} in document id {docId} at index {index}. Exception is {err}"
        gokulam_notation.app.logger.error(error)
        raise Exception(error)


def create_empty_document(client, title):
    '''
    Creates an empty google doc and gives the id

    :param client:
    :param title:
    :return:
    '''
    try:
        gokulam_notation.app.logger.info(f"Attempting to create a new google doc with title {title}")
        result = client.documents().create(body={'title': title}).execute()
        return result["documentId"]
    except Exception as err:
        error = f"Unable to create empty document with title {title}. Exception is {err}"
        gokulam_notation.app.logger.error(error)
        raise Exception(error)

