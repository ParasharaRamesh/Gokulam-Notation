# Contains apis related to google docs
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


def formatText(client, docId, updateTextStyles):
    '''
    :param client:
    :param docId:
    :param updateTextStyles: list of objects where each object is of the form
    {
      'updateTextStyle': {
        'range': {
          'startIndex': int, (inclusive 1 based)
          'endIndex': int (exclusive)
        },
        'fields': '*',
        'textStyle': {
          'bold': boolean,
          'italic': boolean,
          'underline': boolean,
          'backgroundColor': { (This is in case you want to highlight something)
            'color': {
              'rgbColor': {
                'blue': float (0.0 ->1.0),
                'green': float (0.0 ->1.0),
                'red': float (0.0 ->1.0)
              }
            }
          },
          'foregroundColor': { (This is for text color itself)
           'color': {
              'rgbColor': {
                'blue': float (0.0 ->1.0),
                'green': float (0.0 ->1.0),
                'red': float (0.0 ->1.0)
              }
            }
          },
          'fontSize': {
            'magnitude': number,
            'unit': 'PT'
          },
          "baselineOffset": str (possible values SUPERSCRIPT, SUBSCRIPT, NONE, BASELINE_OFFSET_UNSPECIFIED)
        }
      }
    }

    :return:
    '''
    try:
        requests = updateTextStyles
        app.app.logger.info(
            f"Updating the text style in the document with docId {docId} with request body {requests}")
        result = client.documents().batchUpdate(documentId=docId, body={"requests": requests}).execute()
        return result
    except Exception as err:
        error = f"Unable to update the text style in the document with docId {docId} with request body {updateTextStyles}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)

def replaceAllStyleTagsWithEmptyString(client, docId, extractedStyleData):
    '''

    This returns a map of all keys in the request body along with its corresponding closing tag with the values all as empty string

    This is required to replace all of these tags with an empty string later on.

    e.g. {
        "<style:bold,italic>": "",
        "</style:bold,italic>": ""
     }

     then call the replace_values_in_templated_file function

    :param client: docs client
    :param docId: document id
    :param extractedStyleData: return object of extractAllStyleTags function
    :return:
    '''
    try:
        app.app.logger.info(f"Attempting to replace all the style tags {list(extractedStyleData.keys())} in the file with doc id {docId}.")
        templateVars = dict()
        for style in extractedStyleData.keys():
            #NOTE: the opening and closing angular brackets are put in the replace_values_in_templated_file function
            openBracesStyleTag = f"{style}"
            closeBracesStyleTag = f"/{style}"
            templateVars[openBracesStyleTag] = ""
            templateVars[closeBracesStyleTag] = ""
        return replace_values_in_templated_file(client, docId, templateVars)
    except Exception as err:
        error = f"Unable to replace all the style tags {list(extractedStyleData.keys())} in the file with doc id {docId}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)