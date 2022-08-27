# Contains apis related to google sheets
from google_client import *


# main methods
def append_row(sheetsClient, rowData):
    pass


def delete_row(sheetsClient, rowId):
    pass


def read_row(sheetsClient, rowId):
    pass


def update_row(sheetsClient, rowId, newRowData):
    pass


def search(sheetsClient, query):
    pass


# helper methods
def read_excel(sheetsClient, spreadSheetId, spreadSheetRange):
    try:
        # Call the Sheets API
        sheet = sheetsClient.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadSheetId, range=spreadSheetRange).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        return values
    except Exception as err:
        print(err)


if __name__ == "__main__":
    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '14CJ1ftp9MCni4kxHpSnpIg9eyp9VTldO0vzBHLVWtG0'
    #range can be overshot it doest matter!
    RANGE_NAME = 'A1:F1'
    sheetsClient = init_google_sheets_client(True)
    read_excel(sheetsClient, SPREADSHEET_ID, RANGE_NAME)
