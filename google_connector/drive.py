# contains apis related to drive
from constants import DOCUMENT_FILE_TYPE
from google_client import *
from google_connector.docs import create_empty_document


# main methods
def listAllContents(driveClient):
    '''
    lists all of the file contents along with metadata

    :param driveClient:
    :return:
    '''
    results = driveClient.files().list(pageSize=10, fields="nextPageToken, files(*)").execute()
    items = results.get('files', [])
    return items


def create_file(docsClient, driveClient, parentId, relativePathFromParentForFile):
    '''
    Create file in path

    :param driveClient:
    :param parentId:
    :param relativePathFromParentForFile: e.g. /notations/english/shree/endaroMahanubhavulu.gokulam ( NOTE:file types have to end with gokulam)
    :return:
    '''
    try:
        pathComponents = relativePathFromParentForFile.split("/")
        if DOCUMENT_FILE_TYPE not in relativePathFromParentForFile:
            raise Exception(
                f"The path {relativePathFromParentForFile} does not contain the custom file type '.gokulam'. This is required to create a google doc document as specifying other file types will end up creating that particular file type")

        # initially this is the parent id
        nodeId = parentId
        for component in pathComponents:
            isLeaf = DOCUMENT_FILE_TYPE in component
            existingNode = get_node_details_inside_parent(driveClient, component, nodeId)
            if existingNode == None:
                if not isLeaf:
                    # create folder and cd
                    newNodeMetaData = construct_node_metaData(nodeId, component)
                    newNode = create_node(driveClient, newNodeMetaData)
                    nodeId = newNode["id"]
                else:
                    # create document
                    docId = create_empty_document(docsClient, component)
                    # move this file to the current folder ( this is the hack to create a google document inside a drive folder)
                    move_node_to_new_path(driveClient, docId, nodeId)
            elif isLeaf:
                print(f"File with name {component} already exists!")
                return
            else:
                # cd into that folder
                nodeId = existingNode["id"]
    except Exception as err:
        print(f"Error when creating a google doc inside a google drive folder is {err}")


def move_file(driveClient, parentId, oldPath, newPath):
    '''
    Move file from oldPath to newPath

    NOTE: the leaf node name needs to be the same

    :param driveClient:
    :param parentId:
    :param oldPath: 1/2/3/4.gokulam
    :param newPath: 1/2/5/4.gokulam
    :return:
    '''
    try:
        oldNode = get_node_from_path(driveClient, parentId, oldPath)

        # gets the name of the new parent folder under which the file has to go into
        newParentFolderPath = "/".join(newPath.split("/")[:-1])

        newParentNode = get_node_from_path(driveClient, parentId, newParentFolderPath)
        move_node_to_new_path(driveClient, oldNode["id"], newParentNode["id"])
    except Exception as err:
        print(f"Unable to move file from path {oldPath} to new path {newPath}. Exception is {err}")


def delete_node_at_path(driveClient, parentId, relativePathFromParent):
    '''
    Deletes the file passed in the path

    :param driveClient:
    :param parentId:
    :param relativePathFromParent:
    :return:
    '''
    try:
        # get the leaf node
        leafNode = get_node_from_path(driveClient, parentId, relativePathFromParent)
        delete_node(driveClient, leafNode["id"])
        print(f"Deleted successfully")
    except Exception as err:
        print(f"Unable to delete node at path and the error is {err}")


# helper methods
def get_node_details_inside_parent(driveClient, name, parentId):
    '''
    Get node meta data details inside a parent with id

    :param driveClient:
    :param name:
    :param parentId:
    :return:
    '''
    query = f"name='{name}' and '{parentId}' in parents"
    results = driveClient.files().list(q=query, fields="nextPageToken, files(*)").execute()
    if len(results["files"]) != 1:
        print(f"There are no files/folders with the name {name} inside parent folder with id {id}")
        return None
    return results["files"][0]


def construct_node_metaData(parentId, name, isFolder=True):
    '''
    Constructs the node metadata for either a folder or a file

    :param parentId:
    :param name:
    :param isFolder:
    :return:
    '''
    nodeMetaData = {
        "name": name,
        "parents": [parentId]
    }
    if isFolder:
        nodeMetaData["mimeType"] = "application/vnd.google-apps.folder"
    return nodeMetaData


def create_node(driveClient, nodeMetaData):
    """ Create a node and returns the node details
    Returns : Folder itself
    """
    node = None
    try:
        print(f"Trying to create a node in google drive with the metaData {nodeMetaData}")
        node = driveClient.files().create(body=nodeMetaData, fields='*').execute()
        print(f"The node created is {node}")
    except HttpError as error:
        print(F'An error occurred when creating a node: {error}')

    return node


def move_node_to_new_path(driveClient, nodeId, newParentNodeId):
    """Move specified file to the specified folder.
    Args:
        nodeId: Id of the file to move.
        newParentNodeId: Id of the folder
    print: An object containing the new parent folder and other meta data
    """
    try:
        file_id = nodeId
        folder_id = newParentNodeId

        # pylint: disable=maybe-no-member
        # Retrieve the existing parents to remove
        file = driveClient.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = driveClient.files().update(fileId=file_id, addParents=folder_id,
                                          removeParents=previous_parents,
                                          fields='id, parents').execute()

    except HttpError as error:
        raise Exception(f'An error occurred: {error}')

    return file.get('parents')


def delete_node(driveClient, nodeId):
    try:
        driveClient.files().delete(fileId=nodeId).execute()
    except Exception as err:
        print(f'An error occurred when attempting to delete a node: {err}')


def get_node_from_path(driveClient, parentId, relativePathFromParent):
    '''
    Get the node meta data details from the relative path provided

    :param driveClient:
    :param parentId:
    :param relativePathFromParent:
    :return:
    '''
    try:
        pathComponents = relativePathFromParent.split("/")
        # initially this is the parent id
        nodeId = parentId
        existingNode = None
        for component in pathComponents[:-1]:
            # cd into each of the folders
            existingNode = get_node_details_inside_parent(driveClient, component, nodeId)
            if existingNode == None:
                raise Exception(f"Path {relativePathFromParent} does not exist")
            else:
                nodeId = existingNode["id"]
        # get the leaf node
        leafNode = get_node_details_inside_parent(driveClient, pathComponents[-1], nodeId)
        return leafNode
    except Exception as err:
        print(f"Unable to get node from path {relativePathFromParent}, error is {err}")


if __name__ == "__main__":
    testParentId = "1ojiJcePnz62cNR2eGD2pLLxM_RFbfoWX"
    driveClient = init_google_drive_client(True)
    docsClient = init_google_docs_client(True)

    # create_file(docsClient, driveClient, testParentId, "1/2/3/4.gokulam")
    # create_file(docsClient, driveClient, testParentId, "1/2/3/5/6.gokulam")
    move_file(driveClient, testParentId, "1/2/3/4.gokulam", "1/2/3/5/4.gokulam")
