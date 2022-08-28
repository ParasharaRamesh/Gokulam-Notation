import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import app


def extractCredentials(useLocalCreds):
    try:
        if useLocalCreds:
            # this is for local testing if you happen to have the credentials.json file locally!
            localCredsFile = open("credentials.json", "r")
            info = json.load(localCredsFile)
        else:
            # this comes from heroku
            info = json.loads(os.environ['CREDENTIALS'], strict=False)
        return info
    except Exception as err:
        error = f"Unable to extract credentials with useLocalCreds as {useLocalCreds}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def getCredentials(useLocalCreds):
    SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive",
              "https://www.googleapis.com/auth/spreadsheets"]
    credentials = extractCredentials(useLocalCreds)
    creds = service_account.Credentials.from_service_account_info(credentials)
    creds = creds.with_scopes(SCOPES)
    return creds


def init_google_docs_client(useLocalCreds=False):
    try:
        creds = getCredentials(useLocalCreds)
        docs_client = build('docs', 'v1', credentials=creds)
        return docs_client
    except Exception as err:
        app.app.logger.info(err)
        raise Exception(f"Unable to initialize google docs client. Exception is {err}")


def init_google_drive_client(useLocalCreds=False):
    try:
        creds = getCredentials(useLocalCreds)
        drive_client = build('drive', 'v3', credentials=creds)
        return drive_client
    except Exception as err:
        app.app.logger.info(err)
        raise Exception(f"Unable to initialize google drive client. Exception is {err}")


def init_google_sheets_client(useLocalCreds=False):
    try:
        creds = getCredentials(useLocalCreds)
        sheets_client = build('sheets', 'v4', credentials=creds)
        return sheets_client
    except Exception as err:
        app.app.logger.info(err)
        raise Exception(f"Unable to initialize google sheets client. Exception is {err}")
