from server.server import app


@app.route('/')
def index():
    return {'greeting': 'hello world'}
