# contains apis related to drive
from google_client import *

def listAllContents(driveClient):
    results = driveClient.files().list(pageSize=10, fields="nextPageToken, files(*)").execute()
    items = results.get('files', [])
    return items


def create_folder(driveClient):
    """ Create a folder and prints the folder ID
    Returns : Folder Id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    try:
        # create drive api client
        file_metadata = {
            'name': 'Invoices',
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        file = driveClient.files().create(body=file_metadata, fields='id').execute()
        print(F'Folder has created with ID: "{file.get("id")}".')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')

def move_file_to_folder(driveClient, real_file_id, real_folder_id):
    """Move specified file to the specified folder.
    Args:
        real_file_id: Id of the file to move.
        real_folder_id: Id of the folder
    Print: An object containing the new parent folder and other meta data

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        file_id = real_file_id
        folder_id = real_folder_id

        # pylint: disable=maybe-no-member
        # Retrieve the existing parents to remove
        file = driveClient.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = driveClient.files().update(fileId=file_id, addParents=folder_id,
                                      removeParents=previous_parents,
                                      fields='id, parents').execute()

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('parents')


if __name__ == "__main__":
    driveClient = init_google_drive_client(True)
    listAllContents(driveClient)
