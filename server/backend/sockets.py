"""
Defines the socket capabilities for backend, notably joining
and leaving rooms that are 1:1 with puzzles.
"""
from flask import request
from flask_socketio import join_room, leave_room, rooms
from backend import socketio


@socketio.on('connect')
def client_connect():
    """
    Method that is used automatically when a client attempts to open a web socket
    connection with the server.
    """
    print(f"Client with unique session ID {request.sid} has connected...")


@socketio.on('disconnect')
def client_disconnect():
    """
    Method that is used automatically when a client attempts to disconnect
    from a web socket connection with the server.
    """
    print('Client has been disconnected')
    socketio.emit('connected', {'data': 'Connected'})


@socketio.on('join')
def on_join(data):
    """
    Leave a websocket representing a puzzle room; data should be in
    format {puzzle_id: <puzzle_id>}, where puzzle_id represents a "room" that can be
    joined.
    """
    print("This is the data received: " + str(data))
    puzzle_id = data['puzzle_id']
    join_room(room=puzzle_id)
    socketio.emit('left', {"msg": f'Player joined room {puzzle_id}'}, room=puzzle_id)
    print("These are the rooms for user: " + str(rooms()))


@socketio.on('leave')
def on_leave(data):
    """
    Called upon when a client emits an event to leave a puzzle room.
    Expects that data should be in format {puzzle_id: <puzzle_id>}.
    """
    print(data)
    puzzle_id = data['puzzle_id']
    leave_room(puzzle_id)
    socketio.emit('left', {"msg": f'Player left room {puzzle_id}'}, room=puzzle_id)
    print(rooms())
