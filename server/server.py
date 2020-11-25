"""
Use to run server backend application.
"""
from backend import socketio, app

if __name__ == '__main__':
    socketio.run(app, debug=True)
