# all models and types come here
from core.constants.constants import LANGUAGES
from datetime import datetime
from dateutil.tz import gettz


class Notation:
    def __init__(self,
                 name=None,
                 language=LANGUAGES.ENGLISH.value,
                 docLink=None,
                 docId=None,
                 type=None,
                 raga=None,
                 tala=None,
                 composer=None,
                 arohanam=None,
                 avarohanam=None,
                 comments=None,
                 ragaMetaData=None,
                 notatedBy=None,
                 reviewedBy=None,
                 lastModified=str(datetime.now(tz=gettz('Asia/Kolkata'))),
                 workflowEnabled=False):
        self.name = name
        self.language = language
        self.docLink = docLink
        self.docId = docId
        self.type = type
        self.raga = raga
        self.tala = tala
        self.composer = composer
        self.arohanam = arohanam
        self.avarohanam = avarohanam
        self.comments = comments
        self.ragaMetaData = ragaMetaData
        self.notatedBy = notatedBy
        self.reviewedBy = reviewedBy
        self.lastModified = lastModified
        self.workflowEnabled = workflowEnabled

    def __str__(self):
        return f"Notation(workflowEnabled={self.workflowEnabled},name={self.name},language={self.language},docLink={self.docLink},docId={self.docId},type={self.type},raga={self.raga},tala={self.tala},composer={self.composer},arohanam={self.arohanam},avarohanam={self.avarohanam},comments={self.comments},ragaMetaData={self.ragaMetaData},notatedBy={self.notatedBy},reviewedBy={self.reviewedBy},lastModified={self.lastModified}"

    def __repr__(self):
        return f"Notation(workflowEnabled={self.workflowEnabled},name={self.name},language={self.language},docLink={self.docLink},docId={self.docId},type={self.type},raga={self.raga},tala={self.tala},composer={self.composer},arohanam={self.arohanam},avarohanam={self.avarohanam},comments={self.comments},ragaMetaData={self.ragaMetaData},notatedBy={self.notatedBy},reviewedBy={self.reviewedBy},lastModified={self.lastModified}"
