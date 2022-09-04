from flask_restx import Resource, Namespace, fields, reqparse

import logging
import app
from core.constants.constants import LEGEND_SPREADSHEET_ID
from core.google_connector.google_client import init_google_docs_client, init_google_drive_client, \
    init_google_sheets_client
from core.google_connector.sheets import read, delete
from core.models.models import Notation

# initializing all of the various google connector clients
docsClient = init_google_docs_client()
driveClient = init_google_drive_client()
sheetsClient = init_google_sheets_client()

# defining all models and parsers
api = Namespace("notations", description="All endpoints related to notations")

notationModel = api.model("Notation", {
    "name": fields.String(required=False, description="Name of the lesson being notated"),
    "language": fields.String(required=False, description="Language could be (kannada/english)"),
    "docLink": fields.String(required=False, description="Google doc url for the notations"),
    "docId": fields.String(required=True, description="Google doc id"),
    "type": fields.String(required=False, description="Type of the lesson e.g. varnam, kriti etc"),
    "raga": fields.String(required=False, description="Raga the composition is in"),
    "tala": fields.String(required=False, description="Tala the composition is in"),
    "composer": fields.String(required=False, description="The composer of the composition"),
    "arohanam": fields.String(required=False, description="Arohanam of the raga"),
    "avarohanam": fields.String(required=False, description="Avaraohanam of the raga"),
    "comments": fields.String(required=False, description="Optional comments"),
    "ragaMetaData": fields.String(required=False,
                                  description="Additional meta data for raga. e.g. Janyam of 29th melakarta"),
    "notatedBy": fields.String(required=False, description="Name of the person who has contributed"),
    "reviewedBy": fields.String(required=False,
                                description="Name of the person who has reviewed it (can be the same as the contributor)"),
    "lastModified": fields.String(required=False, readonly=True,
                                  description="String representation of the current timestamp. "),
    "workflowEnabled": fields.Boolean(required=False,
                                      description="Boolean field mentioning if review workflow is enabled or not")
})

docIdParser = reqparse.RequestParser()
docIdParser.add_argument("docId", help="Google document id present in the google sheets row", required=True)

# all endpoints
@api.route("")
class Notation(Resource):
    @api.marshal_with(notationModel, skip_none=True)
    @api.doc("Get notation metadata")
    @api.expect(docIdParser)
    def get(self):
        '''
        This endpoint is for getting the notation metadata saved in the google sheets , given a google doc id

        docId is a required url parameter
        :return:
        '''
        app.app.logger.info("Starting get notation endpoint..")
        args = docIdParser.parse_args()
        app.app.logger.info(f"docIdParser args are {args}")
        docId = args["docId"]
        try:
            app.app.logger.info(
                f"Attempting to get the notation row present in the legend spreadsheet for row with doc id {docId}")
            return read(sheetsClient, LEGEND_SPREADSHEET_ID, docId)
        except Exception as err:
            error = f"Attempting to get the notation row present in the legend spreadsheet for row with doc id {docId}"
            app.app.logger.error(error)

    @api.marshal_with(notationModel, skip_none=True)
    @api.expect(docIdParser)
    @api.doc("Remove notation & its associated metadata")
    def delete(self):
        '''
        This is for deleting a notation row in sheets and its corresponding document from docs

        the doc guid can be added as query parameter in the url itself

        this should delete the row in the google sheets and also remove the notation file from the google drive location
        :return:
        '''
        app.app.logger.info("Starting delete notation endpoint..")
        args = docIdParser.parse_args()
        app.app.logger.info(f"docIdParser args are {args}")
        docId = args["docId"]
        try:
            app.app.logger.info(
                f"Attempting to delete the notation row present in the legend spreadsheet for row with doc id {docId}")
            return delete(sheetsClient, LEGEND_SPREADSHEET_ID, docId)
        except Exception as err:
            error = f"Attempting to delete the notation row present in the legend spreadsheet for row with doc id {docId}"
            app.app.logger.error(error)

    @api.marshal_with(notationModel, skip_none=True)
    @api.expect(notationModel, validate=True)
    @api.doc("Create notation doc & associated metadata in google sheets")
    def post(self):
        '''
        This endpoint is for creating a notation row in the google sheets and creating an empty doc in google docs at the specified location

    The request data should have the following information
    {
        "metaData": {
            "language": str(can be kannada or english),
            "lessonName": str,
            "comments": str, (optional)
            "raga": str,
            "arohanam": str,
            "avarohanam": str,
            "ragaMetaData": str,
            "composer": str,
            "tala": str,
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
        2. Create a google doc with the name "lessonName"( provided in metadata) in the google drive path /notations/{language}/{raga}/{tala}/{lessonName}.doc and get the doc link & the doc guid
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
        return "Create notation API"

    @api.marshal_with(notationModel, skip_none=True)
    @api.expect(notationModel, validate=True)
    @api.doc("Update existing notation doc after being notated")
    def put(self):
        '''
        This is for writing the notation into the notation doc

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


@api.route("/metadata")
class NotationMetadata(Resource):
    @api.doc("Update notation metadata")
    @api.expect(notationModel, validate=True)
    @api.marshal_with(notationModel, skip_none=True)
    def put(self):
        '''
        This is for updating the notation metadata in google sheets only

        :return:
        '''
        return "Update metadata"


@api.route("/search", methods=["POST"])
class Search(Resource):
    @api.doc("Search across the notation legend google sheets by using filters")
    @api.expect(notationModel, validate=True)
    @api.marshal_list_with(notationModel, skip_none=True)
    def post(self):
        '''
        This is for querying the worksheet with query strings for searching across each column

    Request body:
    {
        "query": {
            "language": str(can be kannada or english),
            "lessonName": str,
            "comments": str, (optional)
            "raga": str,
            "arohanam": str,
            "avarohanam": str,
            "ragaMetaData": str,
            "composer": str,
            "tala": str,
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
