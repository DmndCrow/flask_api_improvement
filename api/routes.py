from flask import current_app as app


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello world!'
