import logging

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
   return "This is the backend server for the gokulam school notations project"

@app.route("/create-notation", methods = ["POST"])
def createNotation():
    return "Create notation API"

@app.route("/update-notation", methods = ["PUT"])
def updateNotation():
    return "Update notation API"

@app.route("/update-notation-metadata", methods = ["PUT"])
def updateNotationMetadata():
    return "Update notation data API"

@app.route("/delete-notation", methods = ["DELETE"])
def deleteNotationRequest():
    return "Delete notation API"

@app.route("/search", methods = ["POST"])
def search():
    return "Search API"


if __name__ == "__main__":
    app.run(debug=True)

#this is for enabling heroku logging
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)