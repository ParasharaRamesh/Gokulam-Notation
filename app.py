import logging

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
   return "This is the backend server for the gokulam school notations project"

@app.route("/create-notation", methods = ["POST"])
def createNotation():
    '''
    The request data should have the following information
    {
        "metaData": {
            "language": str(can be kannada or english),
            "lessonName": str,
            "comments": str, (optional)
            "raga": str,
            "arohanam": str,
            "avarohanam": str,
            "melakartaParent": str,
            "composer": str,
            "taala": str,
            "type": str (sarali, jantai, varnams, kritis etc), // if it is of type theory then other fields are optional
            "notatedBy": str,
            "reviewedBy" str,
            "lastModifiedDate": unix timestamp ( no need to pass this as the server will take this and populate this with the current timestamp)
        },
        "workflowEnabled": false (if true that would mean that all files have to be reviewed and on successful review only it goes into the actual folder)
    }

    NOTE:
    * for fields which are free text like raga and composer, it should be a dropdown and care should be taken to ensure duplicates dont occur because of minor typos.
    This will help in search later. If it is possible to curate a list of all ragas and  composers ,it will make it easy to leverage the same list in both front end and backend.
    * for the google docs, it might be better to create a template file with variables which can be convieniently replaced rather than inserting

    STEPS:
        1. perform basic validations on request data
        2. Create a google doc with the name "lessonName"( provided in metadata) in the google drive path /notations/{language}/{raga}/{taala}/{lessonName}.doc and get the doc link & the doc guid
        3. In the google doc ensure that the metadata is added directly ( have to experiment to see how to add headings etc). add template markings to add notations
        4. take all the values in the metadata along with the doc guid & doc link and add it in the google sheets as a row
        5. return body {
            "notatedBy": str,
            "status": str ( SUCCESS | FAIL)
            "lastModified": unix timestamp ( milliseconds from 1970 jan 1)
            "docGuid": str,
            "docLink": str,
            "message": str ( if status is FAIL it will contain the error message as is )
        }

    :return: the metadata
    '''
    # data = request.json

    return "Create notation API"

@app.route("/update-notation", methods = ["PUT"])
def updateNotation():
    '''
    The request data should have the following information
    {
        "metaData": {
            "lastModifiedDate": str( this need not be provided in the request body as the server will populate this automatically),
            "docGuid": str
        },
        "notations": {
            "text": str // this is something which requires lots of trial & error,there are google docs which can render color and do formatting,
            have to come up with a custom markdown language which is converted in the backend into the appropriate google docs api
        },
        "workflowEnabled": false (if true it would have to look at the "to be reviewed" folder and then put it into the main folder path)k
    }

    :return:
    {
        "notatedBy": str,
        "lastModified": unix timestamp ( milliseconds from 1970 jan 1)
        "docGuid": str,
        "docLink": str,
        "status": str (SUCCESS | FAIL)
        "message": str (if the status is FAIL it contains the error message as is)
    }

    '''
    return "Update notation API"

@app.route("/update-notation-metadata", methods = ["PUT"])
def updateNotationMetadata():
    return "Update notation data API"

@app.route("/delete-notation", methods = ["DELETE"])
def deleteNotationRequest():
    '''
    the doc guid can be added as query parameter in the url itself

    this should delete the row in the google sheets and also remove the notation file from the google drive location
    :return:
    '''
    return "Delete notation API"

@app.route("/search", methods = ["POST"])
def search():
    '''
    Request body:
    {
        "query": {
            "language": str(can be kannada or english),
            "lessonName": str,
            "comments": str, (optional)
            "raga": str,
            "arohanam": str,
            "avarohanam": str,
            "melakartaParent": str,
            "composer": str,
            "taala": str,
            "type": str (sarali, jantai, varnams, kritis etc), // if it is of type theory then other fields are optional
            "notatedBy": str,
            "reviewedBy" str,
            "lastModifiedDate": unix timestamp ( no need to pass this as the server will take this and populate this with the current timestamp)
        }
    }
    NOTE: this is the same format as the notation metadata, this should ideally use the google sheets api and return all the rows which have matching constraints along with google doc links
    :return:
    '''
    return "Search API"


if __name__ == "__main__":
    app.run(debug=True)

#this is for enabling heroku logging
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)