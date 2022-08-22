import logging

from flask import Flask

from google_connector.google_client import init_google_docs_client
from google_connector.google_docs_experiments import get_document, insert_text_into_document

app = Flask(__name__)

@app.route('/')
def index():
    #this is an experiment to see if heroku environment variables work
    DOCUMENT_ID = '1mGV7Arw8D_QlWhdQPlhnQI3SjV26rcrj1cNDLkzZf-k'

    app.logger.info('Going to init google docs client')
    #Use this if you have local credentials you want to use to try the flow locally
    client = init_google_docs_client()

    document = get_document(client, DOCUMENT_ID)
    app.logger.info('The title of the document is: {}'.format(document.get('title')))

    text = "Testing heroku"
    app.logger.info(f'Going to add [{text}] into the google doc!')
    insert_text_into_document(client, DOCUMENT_ID, text)
    return 'Added text to google docs'

if __name__ == "__main__":
    app.run(debug=True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)