# this will be used for defining all constants
import os
from enum import Enum

SCOPES = ["https://www.googleapis.com/auth/documents",
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/spreadsheets"]
SHEET_NO = 'Sheet1'

LEGEND_SPREADSHEET_ID = os.environ['LEGEND_SPREADSHEET_ID']
PARENT_DRIVE_ID = os.environ['PARENT_DRIVE_ID']

TEMPLATE_NOTATIONS_RELATIVE_PATH_FROM_PARENT_DRIVE_FOLDER = "templates/notationTemplate"

NOTATION_REVIEW_FOLDER = "notations_yet_to_be_reviewed"

class STATUS(Enum):
    IN_PROGRESS = "IN PROGRESS" #when creating
    COMPLETED = "COMPLETED" #when completely finished
    TO_BE_REVIEWED = "TO BE REVIEWED" # when finished but has to be reviewed

class LANGUAGES(Enum):
    ENGLISH = "english"
    KANNADA = "kannada"

STYLE_OPENING_TAG = "<style:"
STYLE_CLOSING_TAG = "</style:"
CLOSING_TAG = ">"
STYLE = "style"