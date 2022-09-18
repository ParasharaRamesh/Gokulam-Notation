# Contains apis related to google docs
'''
TODO:
Implement the following methods:

1. format text https://developers.google.com/docs/api/how-tos/format-text ( make it generic enough for formatting with anystyle)
2. method to delete specific tags ( use the replace all text method and replace with empty string in the end)
3. read document and find all the location of the tags ( give all tags, it should give a Map<tag, list of pairs ( start and end)>, note a tag can be a complex tag with multiple styles together

'''

import app


def get_document(client, docId):
    '''
    Gets a document given docId

    :param client:
    :param docId:
    :return:
    '''
    try:
        app.app.logger.info(f"Getting document details with docId {docId}")
        return client.documents().get(documentId=docId).execute()
    except Exception as err:
        error = f"Unable to get the document with document id {docId}. Exception is {err}"
        app.app.logger.error(error)
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
        app.app.logger.info(
            f"Inserting the text {text} at index {index} in the document with docId {docId} with request body {requests}")
        result = client.documents().batchUpdate(documentId=docId, body={"requests": requests}).execute()
        app.app.logger.info()
        return result
    except Exception as err:
        error = f"Unable to insert text {text} in document id {docId} at index {index}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def create_empty_document(client, title):
    '''
    Creates an empty google doc and gives the id

    :param client:
    :param title:
    :return:
    '''
    try:
        app.app.logger.info(f"Attempting to create a new google doc with title {title}")
        result = client.documents().create(body={'title': title}).execute()
        return result["documentId"]
    except Exception as err:
        error = f"Unable to create empty document with title {title}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def replace_values_in_templated_file(client, templatedDocId, templateVars):
    '''
    Uses the variables in templateVars and replaces the corresponding values in the templated document

    the variables in the google doc will be in the format <var>

    :param client:
    :param templatedDocId:
    :param templateVars: a dictionary with keys and values corresponding to the template variables
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to resolve template variables in the file with doc id {templatedDocId} using templateVars {templateVars}")
        requests = []
        for templateVar, val in templateVars.items():
            requests.append(
                {
                    "replaceAllText": {
                        "replaceText": val,
                        "containsText": {
                            "text": f"<{templateVar}>",
                            "matchCase": True
                        }
                    }
                }
            )

        app.app.logger.info(f"Going to replace the templated variables in the doc {templatedDocId}")
        return client.documents().batchUpdate(documentId=templatedDocId, body={"requests": requests}).execute()
    except Exception as err:
        error = f"Unable to resolve template variables in the file with doc id {templatedDocId} . Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)
