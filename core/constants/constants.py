# this will be used for defining all constants
from enum import Enum

SCOPES = ["https://www.googleapis.com/auth/documents",
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/spreadsheets"]
SHEET_NO = 'Sheet1'


class LANGUAGES(Enum):
    ENGLISH = "english"
    KANNADA = "kannada"
