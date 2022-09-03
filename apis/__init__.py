from flask_restx import Api

from .about import api as aboutNamespace
from .notations import api as notationsNamespace

api = Api(
    title = "Gokulam Notations",
    description = "Backend endpoints for the gokulam notations initiative"
)

api.add_namespace(aboutNamespace)
api.add_namespace(notationsNamespace)