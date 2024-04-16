from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/lists/')
def lists():
    return 'Todo: implement business logic to show all to-do lists'


@app.route('/lists/<int:id>')
def list(id):
    return 'Todo: implement business logic to show all to-dos of a particular list'
