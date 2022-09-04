from flask_restx import Api

from .notations import api as notationsNamespace

api = Api(
    title = "Gokulam Notations",
    description = "Backend endpoints for the gokulam notations initiative"
)

api.add_namespace(notationsNamespace)