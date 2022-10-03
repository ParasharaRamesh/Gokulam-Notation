# Contains apis related to google sheets
from typing import List

from core.constants.constants import SHEET_NO, ALL
from core.models.models import Notation
from core.utils.utils import construct_row_from_notation, construct_notations_from_row, \
    updateNotationWithOnlyFieldsWhichHaveChanged, apply_notation_masks
import app


# main methods
def append(sheetsClient, spreadSheetId, notation: Notation):
    '''
    should append the notationMetaData as a row

    :param sheetsClient:
    :param spreadSheetId:
    :param notation: list of values in the order mentioned in the google sheets
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to append metadata {notation} into spread sheet with id {spreadSheetId}")
        rowIndex = len(get_data(sheetsClient, spreadSheetId))
        return insert_row(sheetsClient, spreadSheetId, rowIndex=rowIndex, notation=notation)
    except Exception as err:
        error = f"Error while attempting to append metadata {notation} into spread sheet with id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def read(sheetsClient, spreadSheetId, docId):
    '''
    should get the notation metadata given docId of the notation

    :param sheetsClient:
    :param spreadSheetId:
    :param docId:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to read metadata from spreadSheet with id {spreadSheetId} for doc with id {docId}")
        data = get_data_as_dataframe(sheetsClient, spreadSheetId)
        if docId != ALL:
            # if we want to fetch only specific doc ids
            mask = data["Google Doc Id"].str.contains(docId, case=True, na=False)
            data = data[mask]
        rows = data.reset_index().to_dict("list")
        return construct_notations_from_row(rows)
    except Exception as err:
        error = f"Error while attempting to read metadata from spreadSheet with id {spreadSheetId} for doc with id {docId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def delete(sheetsClient, spreadSheetId, docId):
    '''
    should delete notation metadata given the docId of the notation

    :param sheetsClient:
    :param spreadSheetId:
    :param docId:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to delete metadata from spreadSheet with id {spreadSheetId} for doc with id {docId}")
        data = get_data_as_dataframe(sheetsClient, spreadSheetId)
        mask = data["Google Doc Id"].str.contains(docId, case=True, na=False)
        row = data[mask]
        # plus 2 because the header is not accounted & it is 1 based indexing
        rowIndex = row.reset_index().to_dict("list")["index"][0] + 2
        return delete_row(sheetsClient, spreadSheetId, rowIndex)
    except Exception as err:
        error = f"Error while attempting to delete metadata from spreadSheet with id {spreadSheetId} for doc with id {docId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def update(sheetsClient, spreadSheetId, newNotation: Notation):
    '''
    should update the notation meta data with the new value.

    Only the values changing will be present here

    :param sheetsClient:
    :param spreadSheetId:
    :param notationMetaData:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to update metadata from spreadSheet with id {spreadSheetId} with new row {newNotation}")
        data = get_data_as_dataframe(sheetsClient, spreadSheetId)
        mask = data["Google Doc Id"].str.contains(newNotation.docId, case=True, na=False)
        row = data[mask].reset_index().to_dict("list")
        # plus 2 because the header is not accounted & it is 1 based indexing
        rowIndex = row["index"][0] + 2
        existingNotation = construct_notations_from_row(row)[0]
        updatedNotation = updateNotationWithOnlyFieldsWhichHaveChanged(existingNotation, newNotation)
        notationRow = construct_row_from_notation(updatedNotation)
        return update_row(sheetsClient, spreadSheetId, rowIndex, notationRow)
    except Exception as err:
        error = f"Error while attempting to update metadata from spreadSheet with id {spreadSheetId} with new row {newNotation}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def search(sheetsClient, spreadSheetId, query: Notation) -> List[Notation]:
    '''
    Given a search query it returns all the rows which match that criteria.
    Implement a really simple search logic ( perhaps convert to dataframe and use pandas)

    :param sheetsClient:
    :param spreadSheetId:
    :param query:
    :return: list of notation objects
    '''
    try:
        app.app.logger.info(
            f"Attempting to search for notations matching query {query} from spreadSheet with id {spreadSheetId}")
        data = get_data_as_dataframe(sheetsClient, spreadSheetId)
        filteredData = apply_notation_masks(data, query)
        searchResults = filteredData.reset_index().to_dict("list")
        app.app.logger.info(f"No of search results {len(searchResults['index'])}")
        return construct_notations_from_row(searchResults)
    except Exception as err:
        error = f"Error while attempting to search for notations matching query {query} from spreadSheet with id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


# helper methods
def construct_worksheet_client(sheetsClient, spreadSheetId):
    '''
    returns a worksheetclient

    :param sheetsClient:
    :param spreadSheetId:
    :return:
    '''
    try:
        app.app.logger.info(f"Attempting to open worksheet with id {spreadSheetId}")
        data = sheetsClient.open_by_key(spreadSheetId)
        return data.worksheet_by_title(SHEET_NO)
    except Exception as err:
        error = f"Error while attempting to open worksheet with id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def insert_row(sheetsClient, spreadSheetId, rowIndex, notation: Notation):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param rowIndex: 0 based indexing
    :param notation: Notation object
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to insert row {notation} into spread sheet with id {spreadSheetId} @ the index(0 based) rowIndex {rowIndex}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        row = construct_row_from_notation(notation)
        app.app.logger.info(f"Appending the row {row}")
        return worksheetClient.insert_rows(rowIndex, values=row)
    except Exception as err:
        error = f"Error while attempting to insert row {notation} into spread sheet with id {spreadSheetId} @ the index(0 based) rowIndex {rowIndex}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def update_row(sheetsClient, spreadSheetId, rowIndex, newRow):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param rowIndex: 1 based indexing
    :param newRow:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to update row {newRow} into spread sheet with id {spreadSheetId} @ the index(1 based) rowIndex {rowIndex}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.update_row(rowIndex, newRow, col_offset=0)
    except Exception as err:
        error = f"Error while attempting to update row {newRow} into spread sheet with id {spreadSheetId} @ the index(1 based) rowIndex {rowIndex}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def update_col(sheetsClient, spreadSheetId, colIndex, newCol):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param colIndex: 1 based indexing
    :param newCol:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to update col {newCol} into spread sheet with id {spreadSheetId} @ the index(1 based) colIndex {colIndex}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.update_col(colIndex, newCol, row_offset=0)
    except Exception as err:
        error = f"Error while attempting to update col {newCol} into spread sheet with id {spreadSheetId} @ the index(1 based) colIndex {colIndex}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def update_cell(sheetsClient, spreadSheetId, rowIndex, colIndex, value):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param rowIndex: 1 based indexing
    :param colIndex: 1 based indexing
    :param value:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to update cell value present at position({rowIndex}, {colIndex}) (1 indexing based) into spread sheet with id {spreadSheetId} with value {value}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.update_value((rowIndex, colIndex), value)
    except Exception as err:
        error = f"Error while attempting to update cell value present at position({rowIndex}, {colIndex}) (1 indexing based) into spread sheet with id {spreadSheetId} with value {value}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def delete_row(sheetsClient, spreadSheetId, rowIndex, noOfRows=1):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param rowIndex: 1 based
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to delete {noOfRows} rows present @ the row index {rowIndex} in spreadsheet with id {spreadSheetId}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.delete_rows(rowIndex, number=noOfRows)
    except Exception as err:
        error = f"Error while Attempting to delete {noOfRows} rows present @ the row index {rowIndex} in spreadsheet with id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def delete_col(sheetsClient, spreadSheetId, colIndex, noOfCols=1):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param colIndex: 1 based
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to delete {noOfCols} columns present @ the column index {colIndex} in spreadsheet with id {spreadSheetId}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.delete_cols(colIndex, number=noOfCols)
    except Exception as err:
        error = f"Error while attempting to delete {noOfCols} cols present @ the column index {colIndex} in spreadsheet with id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def get_row(sheetsClient, spreadSheetId, rowIndex):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param rowIndex:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to get the row present at the index {rowIndex} in the spreadSheet id {spreadSheetId}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.get_row(rowIndex, include_tailing_empty=False)
    except Exception as err:
        error = f"Error while attempting to get the row present at the index {rowIndex} in the spreadSheet id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def get_col(sheetsClient, spreadSheetId, colIndex):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param colIndex:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to get the col present at the index {colIndex} in the spreadSheet id {spreadSheetId}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.get_col(colIndex, include_tailing_empty=False)
    except Exception as err:
        error = f"Error while attempting to get the col present at the index {colIndex} in the spreadSheet id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def get_entire_data(sheetsClient, spreadSheetId):
    '''
    can use get_all_values or can convert to dataframe and then get the entire data frame as is

    :param sheetsClient:
    :param spreadSheetId:
    :return:
    '''
    try:
        app.app.logger.info(f"Attempting to get the entire metadata & data present in spreadSheet id {spreadSheetId}")
        return sheetsClient.sheet.get(spreadSheetId)
    except Exception as err:
        error = f"Error while attempting to get the entire metadata & data present in spreadSheet id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def get_data(sheetsClient, spreadSheetId):
    '''
    can use get_all_values or can convert to dataframe and then get the entire data frame as is

    :param sheetsClient:
    :param spreadSheetId:
    :return:
    '''
    try:
        app.app.logger.info(f"Attempting to get the entire data present in spreadSheet id {spreadSheetId}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
    except Exception as err:
        error = f"Error while attempting to get the entire data present in spreadSheet id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def get_data_as_dataframe(sheetsClient, spreadSheetId):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to get the entire data present in spreadSheet id {spreadSheetId} as a pandas dataframe")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        return worksheetClient.get_as_df(include_tailing_empty=False, include_tailing_empty_rows=False)
    except Exception as err:
        error = f"Error while attempting to get the entire data present in spreadSheet id {spreadSheetId} as a pandas dataframe. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def set_data_as_dataframe(sheetsClient, spreadSheetId, df):
    '''

    :param sheetsClient:
    :param spreadSheetId:
    :param df: dataframe
    :return:
    '''
    try:
        app.app.logger.info(f"Attempting to get the entire data present in spreadSheet id {spreadSheetId}")
        worksheetClient = construct_worksheet_client(sheetsClient, spreadSheetId)
        # setting the entire data as a pandas dataframe
        return worksheetClient.set_dataframe(df, start=(1, 1))
    except Exception as err:
        error = f"Error while attempting to get the entire data present in spreadSheet id {spreadSheetId}. Error is {err}"
        app.app.logger.error(error)
        raise Exception(error)
