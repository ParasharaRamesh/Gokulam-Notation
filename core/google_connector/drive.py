# contains apis related to drive
from core.google_connector.docs import create_empty_document
import app
from core.utils.utils import sanitizePath

# main methods
def listAllContents(driveClient):
    '''
    lists all of the file contents along with metadata

    :param driveClient:
    :return:
    '''
    try:
        app.app.logger.info(f"Trying to list all of the nodes in google drive")
        results = driveClient.files().list(pageSize=10, fields="nextPageToken, files(*)").execute()
        items = results.get('files', [])
        app.app.logger.info(f"The items are {items}")
        return items
    except Exception as err:
        error = f"Unable to get all the nodes from google drive. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def create_drive_node(docsClient, driveClient, parentId, relativePathFromParentForFile,
                      isNewNodeAFile=False,
                      useTemplate=False,
                      relativePathFromParentForTemplateFile=None):
    '''
    Create file in path

    :param driveClient:
    :param parentId:
    :param relativePathFromParentForFile: can be both folders or files
    :param useTemplate: if True then uses the template google doc present in the template path to copy into this
    :param relativePathFromParentForTemplateFile:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Trying to create file in path {relativePathFromParentForFile} in the parent with id {parentId}")
        pathComponents = sanitizePath(relativePathFromParentForFile).split("/")

        # initially this is the parent id
        nodeId = parentId
        for i, component in enumerate(pathComponents):
            isLeaf = (i == len(pathComponents) - 1)
            existingNode = get_node_details_inside_parent(driveClient, component, nodeId)
            if existingNode == None:
                if not isLeaf:
                    app.app.logger.info(f"folder name {component} does not exist! Creating & cd'ing into {component}")
                    # create folder and cd
                    newNodeMetaData = construct_node_metaData(nodeId, component)
                    newNode = create_node(driveClient, newNodeMetaData)
                    nodeId = newNode["id"]
                elif not isNewNodeAFile:
                    app.app.logger.info(f"folder name {component} does not exist! Creating & cd'ing into {component}")
                    # create folder and cd
                    newNodeMetaData = construct_node_metaData(nodeId, component)
                    newNode = create_node(driveClient, newNodeMetaData)
                    nodeId = newNode["id"]
                else:
                    # only if it is a leaf and is a file create or copy it from a preexisting template
                    createDocumentOrCopyFromTemplate(parentId, component, docsClient, driveClient, nodeId, useTemplate,
                                                     relativePathFromParentForTemplateFile)
            elif isLeaf:
                app.app.logger.warn(f"File with name {component} already exists!")
                return
            else:
                # cd into that folder
                app.app.logger.warn(f"folder name {component} already exists! Cd'ing into {component}")
                nodeId = existingNode["id"]
    except Exception as err:
        error = f"Unable to create file in path {relativePathFromParentForFile}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


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
        app.app.logger.info(f"Moving node from path {oldPath} to new path {newPath}")
        oldNode = get_node_from_path(driveClient, parentId, oldPath)
        app.app.logger.info(f"The node from the path {oldPath} is {oldNode}")

        # gets the name of the new parent folder under which the file has to go into
        newParentFolderPath = "/".join(newPath.split("/")[:-1])
        newParentNode = get_node_from_path(driveClient, parentId, newParentFolderPath)
        app.app.logger.info(
            f"The node from the new parent folder path {newParentFolderPath} is {newParentNode}. Now attempting to move the node!")

        # moves the node
        move_node_to_new_path(driveClient, oldNode["id"], newParentNode["id"])
        app.app.logger.info(f"Successfully moved node from path {oldPath} to new path {newPath}")
    except Exception as err:
        error = f"Unable to move node from path {oldPath} to new path {newPath}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def delete_node_at_path(driveClient, parentId, relativePathFromParent):
    '''
    Deletes the file passed in the path

    :param driveClient:
    :param parentId:
    :param relativePathFromParent:
    :return:
    '''
    try:
        app.app.logger.info(f"Trying to delete node at path {relativePathFromParent}")

        # get the leaf node
        leafNode = get_node_from_path(driveClient, parentId, relativePathFromParent)
        app.app.logger.info(f"Retrieved node {leafNode} which has to be deleted! Attempting to delete now..")

        delete_node(driveClient, leafNode["id"])
        app.app.logger.info(f"Deleted node successfully")
    except Exception as err:
        error = f"Unable to delete node at path {relativePathFromParent}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


# helper methods
def createDocumentOrCopyFromTemplate(parentId, name, docsClient, driveClient, targetNodeId, useTemplate,
                                     relativePathFromParentForTemplateFile):
    '''
    Either creates a new google doc or copies from an existing template google doc specified in the template path

    :param parentId:
    :param name:
    :param docsClient:
    :param driveClient:
    :param targetNodeId:
    :param useTemplate:
    :param relativePathFromParentForTemplateFile:
    :return:
    '''
    if not useTemplate:
        # create document
        app.app.logger.info(f"file name {name} does not exist! Creating google doc {name}")
        docId = create_empty_document(docsClient, name)
        # move this file to the current folder ( this is the hack to create a google document inside a drive folder)
        move_node_to_new_path(driveClient, docId, targetNodeId)
        app.app.logger.info(f"Created google doc with name {name} in the location {targetNodeId}!")
    else:
        # copy existing google doc into new parent Node id
        app.app.logger.info(
            f"file name {name} is being created by copying from the template present in relative path {relativePathFromParentForTemplateFile}")
        templateNode = get_node_from_path(driveClient, parentId, relativePathFromParentForTemplateFile)
        copy_node_into_target(driveClient, templateNode["id"], targetNodeId, name)
        app.app.logger.info(
            f"Created google doc with name {name} in the location {targetNodeId} by copying from template present in {relativePathFromParentForTemplateFile}!")


def get_node_details_inside_parent(driveClient, name, parentId):
    '''
    Get node meta data details inside a parent with id

    :param driveClient:
    :param name:
    :param parentId:
    :return:
    '''
    try:
        app.app.logger.info(f"Checking if node with name {name} is present in parent folder with id {parentId}")
        query = f"name='{name}' and '{parentId}' in parents"
        results = driveClient.files().list(q=query, fields="nextPageToken, files(*)").execute()
        if len(results["files"]) != 1:
            app.app.logger.warn(f"There are no files/folders with the name {name} inside parent folder with id {id}")
            return None
        app.app.logger.info(f"Found node with name {name} in parent folder with id {parentId}")
        return results["files"][0]
    except Exception as err:
        error = f"Unable to check if node with name {name} is present in parent folder with id {parentId}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


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
    app.app.logger.info(f"Constructed node meta data {nodeMetaData}")
    return nodeMetaData


def create_node(driveClient, nodeMetaData):
    """ Create a node and returns the node details
    Returns : Folder itself
    """
    try:
        app.app.logger.info(f"Trying to create a node in google drive with the metaData {nodeMetaData}")
        node = driveClient.files().create(body=nodeMetaData, fields='*').execute()
        app.app.logger.info(f"The node created is {node}")
        return node
    except Exception as err:
        error = f"Unable to create a node in google drive with the metaData {nodeMetaData}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def move_node_to_new_path(driveClient, nodeId, newParentNodeId):
    """Move specified file to the specified folder.
    Args:
        nodeId: Id of the file to move.
        newParentNodeId: Id of the folder
    app.app.logger.info: An object containing the new parent folder and other meta data
    """
    try:
        app.app.logger.info(f"Attempting to move node with id {nodeId} into folder with id {newParentNodeId}")
        file_id = nodeId
        folder_id = newParentNodeId

        # Retrieve the existing parents to remove
        file = driveClient.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        app.app.logger.info(f"Retrieved the existing parent to be removed!")

        # Move the file to the new folder
        file = driveClient.files().update(fileId=file_id, addParents=folder_id,
                                          removeParents=previous_parents,
                                          fields='id, parents').execute()
        app.app.logger.info(f"Successfully moved node with id {nodeId} into folder with id {newParentNodeId}")
        return file.get('parents')
    except Exception as err:
        error = f"Unable to to move node with id {nodeId} into folder with id {newParentNodeId}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def delete_node(driveClient, nodeId):
    try:
        app.app.logger.info(f"Attempting to remove node  with id {nodeId}")
        driveClient.files().delete(fileId=nodeId).execute()
    except Exception as err:
        error = f"Unable to delete node with id {nodeId}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def get_node_from_path(driveClient, parentId, relativePathFromParent):
    '''
    Get the node meta data details from the relative path provided

    :param driveClient:
    :param parentId:
    :param relativePathFromParent:
    :return:
    '''
    try:
        app.app.logger.info(f"Attempting to get the node from the relative path {relativePathFromParent}")
        pathComponents = sanitizePath(relativePathFromParent).split("/")
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
        app.app.logger.info(f"Got the leafNode which is {leafNode}")
        return leafNode
    except Exception as err:
        error = f"Unable to get the node from relative path {relativePathFromParent}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)


def copy_node_into_target(driveClient, source_node_id, target_parent_node_id, new_name):
    '''
    Copies the node specified in the source_node_id into the folder with id target_parent_node_id

    :param driveClient:
    :param source_node_id:
    :param target_parent_node_id:
    :param new_name:
    :return:
    '''
    try:
        app.app.logger.info(
            f"Attempting to copy the node with source id {source_node_id} into target node with id {target_parent_node_id} with new name {new_name}")
        return driveClient.files().copy(fileId=source_node_id,
                                        body={"parents": [target_parent_node_id], 'name': new_name}).execute()
    except Exception as err:
        error = f"Unable to copy source node {source_node_id} into target node {target_parent_node_id} with new name {new_name}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)
