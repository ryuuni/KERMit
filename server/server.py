"""
Use to run application, using package
"""
from backend import socketio, app

if __name__ == '__main__':
    socketio.run(app, debug=True)
