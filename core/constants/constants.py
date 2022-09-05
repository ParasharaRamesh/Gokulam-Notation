# this will be used for defining all constants
import os
from enum import Enum

SCOPES = ["https://www.googleapis.com/auth/documents",
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/spreadsheets"]
SHEET_NO = 'Sheet1'

LEGEND_SPREADSHEET_ID = os.environ['LEGEND_SPREADSHEET_ID']

class STATUS(Enum):
    IN_PROGRESS = "IN PROGRESS"
    COMPLETED = "COMPLETED"
    TO_BE_REVIEWED = "TO BE REVIEWED"

class LANGUAGES(Enum):
    ENGLISH = "english"
    KANNADA = "kannada"
