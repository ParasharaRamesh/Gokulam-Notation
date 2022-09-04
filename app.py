import logging
from flask import Flask
from apis import api
from core.google_connector.google_client import init_google_docs_client, init_google_sheets_client, \
    init_google_drive_client

app = Flask(__name__)
api.init_app(app)

docsClient = init_google_docs_client()
driveClient = init_google_drive_client()
sheetsClient = init_google_sheets_client()

if __name__ == "__main__":
    app.run(debug=True)

# this is for enabling heroku logging
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
