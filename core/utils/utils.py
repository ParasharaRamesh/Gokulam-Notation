from typing import List

import app
from core.models.models import Notation


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
