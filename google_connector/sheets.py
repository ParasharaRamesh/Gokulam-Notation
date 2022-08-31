''  # TODO: need to implement all the methods
# Contains apis related to google sheets
from google_client import *
import app


# main methods
def append_row(sheetsClient, rowData):
    pass


def read_row(sheetsClient, rowId):
    pass


def delete_row(sheetsClient, rowId):
    pass


def update_row(sheetsClient, rowId, newRowData):
    pass


def search(sheetsClient, query):
    pass


# helper methods
def read_range(sheetsClient, spreadSheetId, spreadSheetRange):
    try:
        # Call the Sheets API
        sheet = sheetsClient.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadSheetId, range=spreadSheetRange).execute()
        values = result.get('values', [])

        if not values:
            app.app.logger.info('No data found.')
            return
        return values
    except Exception as err:
        app.app.logger.error(err)


def write_range(sheetsClient, spreadSheetId, spreadSheetRange, values, value_input_option="USER_ENTERED"):
    '''
    Write values into range

    :param sheetsClient:
    :param spreadSheetId:
    :param spreadSheetRange:
    :param values: row wise list of lists
    :param value_input_option:
    :return:
    '''
    try:
        body = {
            'values': values
        }
        result = sheetsClient.spreadsheets().values().update(
            spreadsheetId=spreadSheetId, range=spreadSheetRange,
            valueInputOption=value_input_option, body=body).execute()

        return result
    except Exception as error:
        print(f"An error occurred: {error}")
        return error


def append_values(sheetsClient, spreadSheetId, spreadSheetRange, values, value_input_option="USER_ENTERED"):
    body = {
        'values': values
    }
    result = sheetsClient.spreadsheets().values().append(
        spreadsheetId=spreadSheetId, range=spreadSheetRange,
        valueInputOption=value_input_option, body=body).execute()
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
    return result


if __name__ == "__main__":
    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '14CJ1ftp9MCni4kxHpSnpIg9eyp9VTldO0vzBHLVWtG0'
    # range can be overshot it doest matter!
    RANGE_NAME = 'A1:B1'
    sheetsClient = init_google_sheets_client(True)

    values = [
        ['A', 'B'],
        ['C', 'D']
    ]

    appendValues = [
        ['X', 'Y'],
        ['W', 'Z']
    ]
    # write_range(sheetsClient, SPREADSHEET_ID, RANGE_NAME, values)
    append_values(sheetsClient, SPREADSHEET_ID, RANGE_NAME, appendValues)
    # read_excel(sheetsClient, SPREADSHEET_ID, RANGE_NAME)
''
