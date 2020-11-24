""""
FILE FOR DEMONSTRATION PURPOSES ONLY, SHOULD BE REMOVED BEFORE MERGE
"""
import socketio


if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://127.0.0.1:5000')
    print('my sid is', sio.sid)
    sio.emit('connect')
    sio.emit('join', {'puzzle_id': '1'})
