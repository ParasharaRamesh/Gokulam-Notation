from datetime import datetime

from dateutil.tz import gettz
from flask_restx import Resource, Namespace, fields, reqparse, abort
from flask import request

import app
from core.constants.constants import LEGEND_SPREADSHEET_ID, PARENT_DRIVE_ID, \
    TEMPLATE_NOTATIONS_RELATIVE_PATH_FROM_PARENT_DRIVE_FOLDER, NOTATION_REVIEW_FOLDER, STATUS
from core.google_connector.docs import replace_values_in_templated_file, get_document, formatText, \
    replaceAllStyleTagsWithEmptyString
from core.google_connector.drive import delete_node, create_drive_node, copy_node_into_target, move_file
from core.google_connector.google_client import init_google_docs_client, init_google_drive_client, \
    init_google_sheets_client
from core.google_connector.sheets import read, delete, update, search, append
from core.models.models import Notation

# initializing all of the various google connector clients
from core.utils.utils import extractAllStyleTags, constructUpdateTextStyleRequests

docsClient = init_google_docs_client()
driveClient = init_google_drive_client()
sheetsClient = init_google_sheets_client()

# defining all models and parsers
api = Namespace("notations", description="All endpoints related to notations")

notationModel = api.model("Notation", {
    "name": fields.String(required=False, description="Name of the lesson being notated"),
    "language": fields.String(required=False, description="Language could be (kannada/english)"),
    "docLink": fields.String(required=False, description="Google doc url for the notations"),
    "docId": fields.String(required=False, description="Google doc id"),
    "type": fields.String(required=False, description="Type of the lesson e.g. varnam, kriti etc"),
    "notation": fields.String(required=False,
                              description="The entire notation (along with tags) to be written into the google doc"),
    "raga": fields.String(required=False, description="Raga the composition is in"),
    "tala": fields.String(required=False, description="Tala the composition is in"),
    "composer": fields.String(required=False, description="The composer of the composition"),
    "arohanam": fields.String(required=False, description="Arohanam of the raga"),
    "avarohanam": fields.String(required=False, description="Avaraohanam of the raga"),
    "comments": fields.String(required=False, description="Optional comments"),
    "status": fields.String(required=False,
                            description="Status, can take the values (IN PROGRESS, COMPLETED, TO BE REVIEWED)"),
    "ragaMetaData": fields.String(required=False,
                                  description="Additional meta data for raga. e.g. Janyam of 29th melakarta"),
    "notatedBy": fields.String(required=False,
                               description="Name of the person who has contributed, has to be an email id"),
    "reviewedBy": fields.String(required=False,
                                description="Name of the person who has reviewed it (can be the same as the contributor), has to be an email id"),
    "lastModified": fields.String(required=False, description="String representation of the current timestamp. "),
    "pointsToNote": fields.String(required=False, description="Fills the points to note section of the document"),
    "references": fields.String(required=False, description="Fills the references section of the document"),
    "workflowEnabled": fields.Boolean(required=False,
                                      description="Boolean field mentioning if review workflow is enabled or not")
})

docIdParser = reqparse.RequestParser()
docIdParser.add_argument("docId", help="Google document id present in the google sheets row", required=True)


# all endpoints
@api.route("")
class NotationController(Resource):
    @api.expect(docIdParser)
    @api.doc("Remove notation doc & its associated metadata in google sheets")
    def delete(self):
        '''
        This is for deleting a notation row in sheets and its corresponding document from docs

        the doc guid can be added as query parameter in the url itself

        this should delete the row in the google sheets and also remove the notation file from the google drive location. This will however not remove the path of folders

        Note: only docs created from the apis here using the service account can be deleted. Files created manually cannot be deleted as the service account wont be the owner of that file!

        :return:
        '''
        app.app.logger.info("Starting delete notation endpoint..")
        args = docIdParser.parse_args()
        docId = args["docId"]
        try:
            app.app.logger.info(f"Now attempting to delete the doc with {docId} ")
            delete_node(driveClient, docId)
            app.app.logger.info(
                f"Successfully deleted the google doc with id {docId}. Now attempting to delete the notation row present in the legend spreadsheet")
            delete(sheetsClient, LEGEND_SPREADSHEET_ID, docId)
            app.app.logger.info(f"Successfully deleted the row with the doc id {docId} in the legend spreadsheet!!")
            return {
                       "message": f"Successfully deleted the doc & the row with the doc id {docId} in the legend spreadsheet!!"
                   }, 200
        except Exception as err:
            error = f"Failure when attempting to delete the notation with doc id {docId}. Exception is {err}"
            app.app.logger.error(error)
            return abort(message=error)

    @api.expect(notationModel, validate=True)
    @api.doc("Create notation doc & associated metadata in google sheets")
    def post(self):
        '''
        This endpoint is for creating a notation row in the google sheets and creating an empty doc in google docs at the specified location

        The status becomes IN PROGRESS after this.

        NOTE: this does not fill anything in the document at this point. Therefore only fill the fields which are present in the spreadsheet.

        :return: message string
        '''
        app.app.logger.info("Starting create notation endpoint..")
        data = request.json
        notation = Notation(**data)
        app.app.logger.info(f"create notation request is {notation}")
        try:
            pathToCreateTemplateFile = f"{notation.language}/{notation.type}/{notation.raga}/{notation.tala}/{notation.name}"
            if notation.workflowEnabled:
                # if workflow is enabled it has to be created here!
                pathToCreateTemplateFile = f"{NOTATION_REVIEW_FOLDER}/{pathToCreateTemplateFile}"

            app.app.logger.info(f"Attempting to create a template notation file at the path {pathToCreateTemplateFile}")
            docId = create_drive_node(docsClient, driveClient, PARENT_DRIVE_ID, pathToCreateTemplateFile, True, True,
                                      TEMPLATE_NOTATIONS_RELATIVE_PATH_FROM_PARENT_DRIVE_FOLDER)

            # updating the notation with new doc id and doc link which was created
            notation.docId = docId
            notation.docLink = f"https://docs.google.com/document/d/{docId}/edit"
            notation.status = STATUS.IN_PROGRESS.value

            app.app.logger.info(
                f"Created template file @ path {pathToCreateTemplateFile} with doc id {docId}. Now adding metadata to legend spreadsheet!")
            append(sheetsClient, LEGEND_SPREADSHEET_ID, notation)
            app.app.logger.info(f"Added notation row {notation} in the legend spread sheet!")
            return {
                       "message": f"Successfully created document at path {pathToCreateTemplateFile} with doc id {docId} & also inserted metadata row in the legend spreadsheet!",
                       "docId": docId
                   }, 200
        except Exception as err:
            error = f"Failure when attempting to create the notation with create notation request {notation}. Exception is {err}"
            app.app.logger.error(error)
            return abort(message=error)

    @api.expect(notationModel, validate=True)
    @api.doc("Update existing notation doc after being notated")
    def put(self):
        '''
        This is for writing the notation into the notation doc

        NOTE: In case there are any edits to the file, they can navigate directly to the doc and edit it!

        The status becomes COMPLETED or TO BE REVIEWED based on whether the workflow is active or not

        The request needs to contain only docId and other details which have to be filled in the template file
        '''
        app.app.logger.info("Starting write notation endpoint..")
        data = request.json
        notation = Notation(**data)
        app.app.logger.info(f"write notation request is {notation}")
        docId = notation.docId
        workflowEnabled = notation.workflowEnabled
        try:
            # removing the doc id  in order to create a dictionary of template variables!
            notation.docId = None
            notation.workflowEnabled = None
            templateVars = notation.__dict__
            replace_values_in_templated_file(docsClient, docId, templateVars)

            app.app.logger.info(f"Finished writing into doc id {docId} now updating the styles by parsing the notation tags and by performing a batch update")

            docsData = get_document(docsClient, docId)
            extractedStyleData = extractAllStyleTags(docsData)
            constructedUpdateStyleRequestData = constructUpdateTextStyleRequests(extractedStyleData)
            formatText(docsClient, docId, constructedUpdateStyleRequestData)
            replaceAllStyleTagsWithEmptyString(docsClient, docId, extractedStyleData)

            # update the sheets with correct status based on workflow enabled flag
            if workflowEnabled:
                app.app.logger.info(
                    f"Finished updating the styles into doc with doc id {docId}. Now changing the status in legend spreadsheet with id {STATUS.TO_BE_REVIEWED.value} as workflow is enabled!")
                update(sheetsClient, LEGEND_SPREADSHEET_ID, Notation(docId=docId, status=STATUS.TO_BE_REVIEWED.value,
                                                                     lastModified=str(
                                                                         datetime.now(tz=gettz('Asia/Kolkata')))))
            else:
                app.app.logger.info(
                    f"Finished updating the styles into doc with doc id {docId}. Now changing the status in legend spreadsheet with id {STATUS.COMPLETED.value}")
                update(sheetsClient, LEGEND_SPREADSHEET_ID, Notation(docId=docId, status=STATUS.COMPLETED.value,
                                                                     lastModified=str(
                                                                         datetime.now(tz=gettz('Asia/Kolkata')))))

            return {
                       "message": f"Successfully updated the doc with id {docId} with template vars {templateVars}. Updated the status appropriately!"
                   }, 200
        except Exception as err:
            error = f"Failure when attempting to write the notation {notation} into doc file with doc id {notation.docId}. Exception is {err}"
            app.app.logger.error(error)
            return abort(message=error)


@api.route("/workflow")
class NotationMetadataController(Resource):
    @api.doc("Move created document from the to be reviewed folder to the actual folder after reviews are completed!")
    @api.expect(docIdParser)
    def get(self):
        '''
        Given docId which is under review (i.e. if the workflow approval is active), it gets the metadata from the google sheets and uses the to be reviewed location derived from the rows to put it into another folder

        The status becomes COMPLETED after this from TO BE REVIEWED.

        :return:
        '''
        app.app.logger.info("Starting approval workflow which moves the document")
        args = docIdParser.parse_args()
        docId = args["docId"]
        try:
            app.app.logger.info(
                f"Attempting to get the notation row present in the legend spreadsheet for row with doc id {docId}")
            notationRow = read(sheetsClient, LEGEND_SPREADSHEET_ID, docId)
            app.app.logger.info(
                f"retrieved row {notationRow} for the document which has to be approved!. Now moving to actual location")
            oldPathFromRow = f"{NOTATION_REVIEW_FOLDER}/{notationRow.language}/{notationRow.type}/{notationRow.raga}/{notationRow.tala}/{notationRow.name}"
            newApprovedPath = f"{notationRow.language}/{notationRow.type}/{notationRow.raga}/{notationRow.tala}/{notationRow.name}"
            move_file(docsClient, driveClient, PARENT_DRIVE_ID, oldPath=oldPathFromRow, newPath=newApprovedPath)
            app.app.logger.info(
                f"moved the document from {oldPathFromRow} to {newApprovedPath}. Now changing metadata with status as COMPLETED")
            update(sheetsClient, LEGEND_SPREADSHEET_ID, Notation(docId=notationRow.docId, status=STATUS.COMPLETED.value,
                                                                 lastModified=str(
                                                                     datetime.now(tz=gettz('Asia/Kolkata')))))
            app.app.logger.info(f"updated the metadata for row with id {docId} with status as COMPLETED")
            return {
                       "message": f"Successfully approved the doc with docId {notationRow.docId} by moving to correct location and changed the status in the legend spreadsheet!!"
                   }, 200
        except Exception as err:
            error = f"Failure when attempting to perform approval workflow on doc with docId {docId}. Exception is {err}"
            app.app.logger.error(error)
            return abort(message=error)


@api.route("/metadata")
class NotationMetadataController(Resource):
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
        docId = args["docId"]
        try:
            app.app.logger.info(
                f"Attempting to get the notation row present in the legend spreadsheet for row with doc id {docId}")
            notation = read(sheetsClient, LEGEND_SPREADSHEET_ID, docId)
            # if the status is to be reviewed then we know that workflow is enabled!
            notation.workflowEnabled = notation.status == STATUS.TO_BE_REVIEWED
            return notation
        except Exception as err:
            error = f"Failure when attempting to get the notation row present in the legend spreadsheet for row with doc id {docId}. Exception is {err}"
            app.app.logger.error(error)
            return abort(message=error)

    @api.doc("Update notation metadata")
    @api.expect(notationModel, validate=True)
    @api.marshal_with(notationModel, skip_none=True)
    def put(self):
        '''
        This is for updating the notation metadata in google sheets only

        :return:
        '''
        app.app.logger.info("Starting update notation metadata..")
        try:
            data = request.json
            app.app.logger.info(f"request is {data}")
            notation = Notation(**data)
            notation.lastModified = str(datetime.now(tz=gettz('Asia/Kolkata')))
            app.app.logger.info(
                f"Attempting to update the notation metadata row present in the legend spreadsheet with notation {notation}")
            return update(sheetsClient, LEGEND_SPREADSHEET_ID, notation)
        except Exception as err:
            error = f"Failure when attempting to update the notation metadata present in the legend spreadsheet with notation {notation}. Exception is {err}"
            app.app.logger.error(error)
            return abort(message=error)


@api.route("/search", methods=["POST"])
class SearchController(Resource):
    @api.doc("Search across the notation legend google sheets by using filters")
    @api.expect(notationModel, validate=True)
    @api.marshal_list_with(notationModel, skip_none=True)
    def post(self):
        '''
        This is for querying the worksheet with query strings for searching across each column

        :return:
        '''
        app.app.logger.info("Starting search notation metadata api..")
        try:
            data = request.json
            app.app.logger.info(f"request is {data}")
            query = Notation(**data)
            # last modified needs to be explicitly present in request data for it to be filtered
            if "lastModified" not in data:
                query.lastModified = None
            app.app.logger.info(
                f"Attempting to search in the legend spreadsheet with query {query}")
            return search(sheetsClient, LEGEND_SPREADSHEET_ID, query)
        except Exception as err:
            error = f"Failure when attempting to search in the legend spreadsheet with query {query}. Exception is {err}"
            app.app.logger.error(error)
            return abort(message=error)
