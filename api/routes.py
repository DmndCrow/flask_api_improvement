from flask import current_app as app


@app.route('/', methods=['GET'])
def root():
    return 'Root'


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello world!'
