
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

flask_app = Flask(__name__)

@flask_app.route('/')
def hello_world():
    return 'Hello from Flask!'

