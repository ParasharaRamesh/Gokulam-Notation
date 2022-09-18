import logging
from flask import Flask

#NOTE: comment out the import statement from apis and the line 'api.init_app' for running experiements locally
from apis import api

app = Flask(__name__)
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)

# this is for enabling heroku logging
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
