from flask_restx import Api, Resource, Namespace

api = Namespace("about", description="About")

@api.route("/")
class AboutController(Resource):
    def get(self):
        return "This is the backend server for the gokulam school notations project!!"