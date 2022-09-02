# Contains apis related to google sheets
from google_client import *
import app

# main methods
def append(sheetsClient, spreadSheetId, notationMetaData):
    '''
    should append the notationMetaData as a row

    :param sheetsClient:
    :param spreadSheetId:
    :param notationMetaData:
    :return:
    '''
    pass


def read(sheetsClient, spreadSheetId, docId):
    '''
    should get the notation metadata given docId of the notation

    :param sheetsClient:
    :param spreadSheetId:
    :param docId:
    :return:
    '''
    pass


def delete(sheetsClient, spreadSheetId, docId):
    '''
    should delete notation metadata given the docId of the notation

    :param sheetsClient:
    :param spreadSheetId:
    :param docId:
    :return:
    '''
    pass


def update(sheetsClient, spreadSheetId, notationMetaData):
    '''
    should update the notation meta data with the new value.

    Only the values changing will be present here

    :param sheetsClient:
    :param spreadSheetId:
    :param notationMetaData:
    :return:
    '''
    pass


def search(sheetsClient, spreadSheetId, query):
    '''
    Given a search query it returns all the rows which match that criteria.
    Implement a really simple search logic ( perhaps convert to dataframe and use pandas)

    :param sheetsClient:
    :param spreadSheetId:
    :param query:
    :return:
    '''
    pass


# helper methods
def insert_row(spreadSheetId, rowIndex, row):
    '''

    :param spreadSheetId:
    :param rowIndex: 0 based indexing
    :param row: list of values
    :return:
    '''
    pass

def update_row(spreadSheetId, rowIndex, newRow):
    '''

    :param spreadSheetId:
    :param rowIndex: 1 based indexing
    :param newRow:
    :return:
    '''
    pass

def update_cell(spreadSheetId, rowIndex, columnIndex, value):
    '''

    :param spreadSheetId:
    :param rowIndex: 1 based indexing
    :param columnIndex: 1 based indexing
    :param value:
    :return:
    '''
    pass

def delete_row(spreadSheetId, rowIndex):
    '''

    :param spreadSheetId:
    :param rowIndex: 1 based
    :return:
    '''
    pass

def get_row(spreadSheetId, rowIndex):
    '''

    :param spreadSheetId:
    :param rowIndex:
    :return:
    '''
    pass

def get_entire_data(spreadSheetId):
    '''
    can use get_all_values or can convert to dataframe and then get the entire data frame as is

    :param spreadSheetId:
    :return:
    '''
    pass

if __name__ == "__main__":
    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '14CJ1ftp9MCni4kxHpSnpIg9eyp9VTldO0vzBHLVWtG0'

    sheetsClient = init_google_sheets_client_using_pygsheets(True)

    # read all data
    # data = sheetsClient.sheet.get(SPREADSHEET_ID)

    # open by id
    data = sheetsClient.open_by_key(SPREADSHEET_ID)
    wks = data.worksheet_by_title('Sheet1')

    # get all data as list of lists ( row wise)
    # values = wks.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)

    # get row ( 1 indexing)
    # row = wks.get_row(1, include_tailing_empty=False)

    # get column ( 1 indexing)
    # col = wks.get_col(1, include_tailing_empty=False)

    # get as pandas dataframe ( considers 1st row as heading )
    # sdf = wks.get_as_df(include_tailing_empty=False, include_tailing_empty_rows=False)

    # delete row ( does exactly what I want)
    # wks.delete_rows(1, number=1)

    # delete cols ( does exactly what I want)
    # wks.delete_cols(1, number=1)

    # insert column(0 based indexing)
    # result = wks.insert_cols(2, values=["1", "2","3"])

    # insert row(0 based indexing)
    # result = wks.insert_rows(5, values=["1", "2","3"])

    # update row ( 1 based indexing)
    # wks.update_row(1, ["s", "e", "m"], col_offset=0)

    # update col ( 0 based indexing)
    # wks.update_col(1, ["a", "b", "c"], row_offset=0)

    # update cell
    # wks.update_value('A1', "testing")
    # wks.update_value((1,1), "shatas")

    pass
    # set dataframe
    # wks.set_dataframe(df, start=(1,1))
