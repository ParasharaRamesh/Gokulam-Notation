# all models and types come here
from core.constants.constants import LANGUAGES
from datetime import datetime
from dateutil.tz import gettz

class Notation:
    def __init__(self,
                 name=None,
                 language=LANGUAGES.ENGLISH,
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
                 lastModified=datetime.now(tz=gettz('Asia/Kolkata'))):
        self.name = name
        self.language = language
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
