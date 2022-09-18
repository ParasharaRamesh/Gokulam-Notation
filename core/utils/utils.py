from typing import List
import app
from core.constants.constants import STYLE_CLOSING_TAG, STYLE_OPENING_TAG, CLOSING_TAG, STYLE
from core.models.models import Notation
import re

def isStringEmpty(str):
    return (str == None) or (len(str) == 0)


def sanitizePath(path):
    '''
    incase the path starts with a / then it just removes it

    eg. /a/b -> a/b

    This is so that other functions can work as expected

    :param path:
    :return:
    '''
    if path[0] == "/":
        return path[1:]
    return path

#this order comes from the google sheet being used
def construct_row_from_notation(notation: Notation):
    return [
        notation.type,
        notation.name,
        notation.language,
        notation.raga,
        notation.tala,
        notation.composer,
        notation.docId,
        notation.docLink,
        notation.notatedBy,
        notation.reviewedBy,
        notation.lastModified,
        notation.status
    ]


def construct_notations_from_row(row) -> List[Notation]:
    notations = []
    for i in range(len(row["index"])):
        notations.append(Notation(
            type=row["Type"][i],
            name=row["Name"][i],
            language=row["Language"][i],
            raga=row["Raga"][i],
            tala=row["Tala"][i],
            composer=row["Composer"][i],
            docId=row["Google Doc Id"][i],
            docLink=row["Google Doc Link"][i],
            notatedBy=row["Notated By"][i],
            reviewedBy=row["Reviewed By"][i],
            lastModified=row["Last Modified Date"][i],
            status=row["Status"][i]
        ))
    return notations


def updateNotationWithOnlyFieldsWhichHaveChanged(existingNotation: Notation, newNotation: Notation) -> Notation:
    if not isStringEmpty(newNotation.name) and existingNotation.name != newNotation.name:
        existingNotation.name = newNotation.name

    if not isStringEmpty(newNotation.language) and existingNotation.language != newNotation.language:
        existingNotation.language = newNotation.language

    if not isStringEmpty(newNotation.raga) and existingNotation.raga != newNotation.raga:
        existingNotation.raga = newNotation.raga

    if not isStringEmpty(newNotation.tala) and existingNotation.tala != newNotation.tala:
        existingNotation.tala = newNotation.tala

    if not isStringEmpty(newNotation.composer) and existingNotation.composer != newNotation.composer:
        existingNotation.composer = newNotation.composer

    if not isStringEmpty(newNotation.docId) and existingNotation.docId != newNotation.docId:
        existingNotation.docId = newNotation.docId

    if not isStringEmpty(newNotation.docLink) and existingNotation.docLink != newNotation.docLink:
        existingNotation.docLink = newNotation.docLink

    if not isStringEmpty(newNotation.notatedBy) and existingNotation.notatedBy != newNotation.notatedBy:
        existingNotation.notatedBy = newNotation.notatedBy

    if not isStringEmpty(newNotation.reviewedBy) and existingNotation.reviewedBy != newNotation.reviewedBy:
        existingNotation.reviewedBy = newNotation.reviewedBy

    if not isStringEmpty(newNotation.lastModified) and existingNotation.lastModified != newNotation.lastModified:
        existingNotation.lastModified = newNotation.lastModified

    if not isStringEmpty(newNotation.status) and existingNotation.status != newNotation.status:
        existingNotation.status = newNotation.status

    return existingNotation


def apply_notation_masks(data, query: Notation):
    if not isStringEmpty(query.docId):
        app.app.logger.info("Doc id column is being filtered..")
        mask = data["Google Doc Id"].str.contains(query.docId, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.type):
        app.app.logger.info("Type column is being filtered..")
        mask = data["Type"].str.contains(query.type, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.name):
        app.app.logger.info("Name column is being filtered..")
        mask = data["Name"].str.contains(query.name, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.language):
        mask = data["Language"].str.contains(query.language, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.raga):
        app.app.logger.info("Raga column is being filtered..")
        mask = data["Raga"].str.contains(query.raga, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.tala):
        app.app.logger.info("Tala column is being filtered..")
        mask = data["Tala"].str.contains(query.tala, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.composer):
        app.app.logger.info("Composer column is being filtered..")
        mask = data["Composer"].str.contains(query.composer, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.docLink):
        app.app.logger.info("Doc link column is being filtered..")
        mask = data["Google Doc Link"].str.contains(query.docLink, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.notatedBy):
        app.app.logger.info("Notated by column is being filtered..")
        mask = data["Notated By"].str.contains(query.notatedBy, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.reviewedBy):
        app.app.logger.info("Reviewed by column is being filtered..")
        mask = data["Reviewed By"].str.contains(query.reviewedBy, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.lastModified):
        app.app.logger.info("Last modified column is being filtered..")
        mask = data["Last Modified Date"].str.contains(query.lastModified, case=False, na=False)
        data = data[mask]

    if not isStringEmpty(query.status):
        app.app.logger.info("Status column is being filtered..")
        mask = data["Status"].str.contains(query.status, case=False, na=False)
        data = data[mask]

    return data

def constructUpdateTextStyleRequests(extractedStyleData):
    '''
    e.g. the input data can be like
    {
        "style:bold": [(1,2), (3,4)],
        "style:italic,underline": [(10,20), (30,40)],
        "style:bold,italic,underline": [(45,50)],
        "style:fontSize-16": [(55,60)],
        "style:baselineOffset-SUBSCRIPT": [(65,70)],
        "style:baselineOffset-SUPERSCRIPT,fontSize-19": [(75,80)],
        "style:backgroundColor-0.0|0.8|0.87": [(85,90)],
        "style:backgroundColor-0.0|0.8|0.87,foregroundColor-1.0|0.8|0.87": [(91,100)]
    }

    :param extractedStyleData: return object of extractAllStyleTags function
    :return: list of updateTextStyle objects ( refer to docs file to see the request object)
    '''
    requests = []
    for style, ranges in extractedStyleData.items():
        compositeStyles = style.split(":")[1]
        individualStyles = compositeStyles.split(",")
        for updateRange in ranges:
            request = initUpdateTextStyleRequest()
            request["updateTextStyle"]["range"]["startIndex"] = updateRange[0]
            request["updateTextStyle"]["range"]["endIndex"] = updateRange[1]
            for individualStyle in individualStyles:
                isStyleWithParams = "-" in individualStyle
                if not isStyleWithParams:
                    request["updateTextStyle"]["textStyle"][individualStyle] = True
                else:
                    parameterizedStyle, params = individualStyle.split("-")
                    individualParams = params.split("|")
                    if parameterizedStyle == "baselineOffset":
                        request["updateTextStyle"]["textStyle"][parameterizedStyle] = individualParams[0]
                    elif parameterizedStyle == "fontSize":
                        request["updateTextStyle"]["textStyle"][parameterizedStyle] = {
                            "unit": "PT",
                            "magnitude": int(individualParams[0])
                        }
                    elif parameterizedStyle in ["backgroundColor", "foregroundColor"]:
                        request["updateTextStyle"]["textStyle"][parameterizedStyle] = {
                            "color": {
                                "rgbColor": {
                                    "red": float(individualParams[0]),
                                    "green": float(individualParams[1]),
                                    "blue": float(individualParams[2])
                                }
                            }
                        }
            requests.append(request)
    return requests

def initUpdateTextStyleRequest():
    '''
    Constructs an empty updateTextStyleRequest object

    :return:
    '''
    return {
        "updateTextStyle": {
            "fields": "*",
            "textStyle": {},
            "range": {}
        }
    }

def extractAllStyleTags(docsData):
    '''
    Extract all possible style tags and return data in the following format:

    Map<compositeStyle, list of pairs of start and end index>

    composite style could be tags where there are more than one style applied

    :param docsData: json data from google docs
    :return:
    '''
    try:
        docId = docsData["documentId"]
        app.app.logger.info(f"Extracting the style tags from the document with doc id {docId}")
        allStyles = dict()

        #get only the paragraph contents
        contents = list(filter(lambda content: "paragraph" in content, docsData["body"]["content"]))
        for content in contents:
            paragraphElements = content["paragraph"]["elements"]
            paragraphStartIndex = None
            text = ""
            paragraphElementsTextContents = list(map(lambda paragraphElement: paragraphElement["textRun"]["content"] , paragraphElements))
            isStyled = len(list(filter(lambda content: STYLE in content, paragraphElementsTextContents))) > 0
            if isStyled:
                for i, paragraphElement in enumerate(paragraphElements):
                    # this is required because sometimes the same line can be broken up into multiple paragraph elements. Therefore collating everything
                    if i == 0:
                        paragraphStartIndex = paragraphElement["startIndex"]
                    text += paragraphElement["textRun"]["content"]

                #now we have the line with all the style tags, now we have to add it to our allStyles dict after figuring out the starting and ending index
                if paragraphStartIndex != None:
                    allStyleOpeningTagPositions = [m.start() for m in re.finditer(STYLE_OPENING_TAG, text)]
                    allStyleClosingTagPositions = [m.start() for m in re.finditer(STYLE_CLOSING_TAG, text)]

                    assert(len(allStyleOpeningTagPositions) == len(allStyleClosingTagPositions))

                    for styleOpeningPosition, styleClosingPosition in zip(allStyleOpeningTagPositions, allStyleClosingTagPositions):
                        # find the index of the closest closing tag ">" from the opening style bracket
                        indexForClosingAngularTagForOpeningStyleTag = styleOpeningPosition
                        while indexForClosingAngularTagForOpeningStyleTag <= styleClosingPosition:
                            if text[indexForClosingAngularTagForOpeningStyleTag] == CLOSING_TAG:
                                break
                            indexForClosingAngularTagForOpeningStyleTag += 1

                        #style tag is the sliced string inside this tag
                        style = text[styleOpeningPosition + 1: indexForClosingAngularTagForOpeningStyleTag]

                        # plus 1 to account for "/" and plus 2 to account for ">" and extra one more for exclusivity in range
                        styleRange = (paragraphStartIndex + styleOpeningPosition, paragraphStartIndex + styleClosingPosition + 1 + len(style) + 2)
                        if style not in allStyles:
                            allStyles[style] = [styleRange]
                        else:
                            allStyles[style].append(styleRange)

        return allStyles
    except Exception as err:
        error = f"Unable to extract the style tags from the document with doc id {docId}. Exception is {err}"
        app.app.logger.error(error)
        raise Exception(error)

