import logging
from flask import Flask
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
