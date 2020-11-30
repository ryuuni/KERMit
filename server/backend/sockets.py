"""
Defines the socket capabilities for backend, notably joining
and leaving rooms that are 1:1 with puzzles and being able to
send messages between users of the same puzzle.
"""
from flask import request
from flask_socketio import join_room, leave_room, rooms
from backend.models.player import PuzzlePlayer
from backend.models.user import User
from backend import socketio
from backend.models.sudoku_puzzle import Puzzle
from backend.resources.authentication import is_valid_token
from backend.resources.sudoku_puzzle import sudoku_to_dict


@socketio.on('connect')
def client_connect():
    """
    Method that is used automatically when a client attempts to open a web socket
    connection with the server. In order to establish the connection,
    a oauth token must be provided and it must be valid according to the Google API.
    Note that if the token is not valid, the
    """
    oauth_token = request.args.get('auth')
    if not oauth_token:
        print("Oauth token missing from web socket connection request")
        return False

    is_valid, validation = is_valid_token(oauth_token)
    if not is_valid:
        print(f"Supplied oauth token is not valid: {validation['error_description']}")
        return False

    print(f"Client with unique session ID {request.sid} has connected...")
    return True


@socketio.on('disconnect')
def client_disconnect():
    """
    Method that is used automatically when a client attempts to disconnect
    from a web socket connection with the server.
    """
    print(f'Client with session ID {request.sid} has been disconnected')
    socketio.emit('disconnect', {'msg': 'Client disconnected'}, room=request.sid)


@socketio.on('join')
def on_join(data):
    """
    Leave a websocket representing a puzzle room; data should be in format
    {puzzle_id: <puzzle_id>, token: <oauth_token>}, where puzzle_id represents
    a "room" that can be joined. Note that users can only entire web socket "rooms" if they
    are, in fact, associated with a puzzle.
    """
    if any(key not in data.keys() for key in ['token', 'puzzle_id']):
        return False

    # find out who user is
    is_valid, validation = is_valid_token(data['token'])
    if not is_valid:
        return False

    # find the user in our system; if they do not exist, do not do anything
    user = User.find_by_g_id(validation['user_id'])
    if not user:
        return False

    # make sure that they can join the room, based on the puzzles they
    # are participating in
    puzzle_id = int(data['puzzle_id'])
    player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(user.g_id)
    if not any(puzzle.puzzle_id == puzzle_id for puzzle in player_puzzles):
        return False

    join_room(room=puzzle_id)
    socketio.emit('player_joined', {"msg": f'Player joined room {puzzle_id}'}, room=puzzle_id)
    return True


@socketio.on('move')
def on_move(data):
    """
    Handles announcement of a move on the puzzle board for puzzle piece.
    """
    print("A move was submitted by a user!")
    if 'puzzle_id' not in data.keys():
        return

    puzzle_id = int(data['puzzle_id'])
    puzzle = Puzzle.get_puzzle(puzzle_id)
    socketio.emit('puzzle_update', sudoku_to_dict(puzzle), room=puzzle_id)
    return True


@socketio.on('message')
def on_message(data):
    """
    Handles announcement of a new message sent to users on the
    puzzle board. Emits the message to all people who are currently in the puzzle
    "room" at the time.
    """
    if 'puzzle_id' not in data.keys():
        return

    print("A new message was sent by a user!")
    socketio.emit('message_update', data, room=int(data['puzzle_id']))


@socketio.on('add_lock')
def on_lock(data):
    """
    In order to prevent users from working on the same puzzle piece at the same
    time, the frontend can emit "add_lock" events, which will be routed here
    to all currently members of the puzzle to prevent others from acting on that
    piece at the same time.
    """
    if 'puzzle_id' not in data.keys():
        return

    print(f"A new lock should be created; client with "
          f"session ID {request.sid} is making a move.")
    socketio.emit('lock_update_add', data, room=int(data['puzzle_id']))


@socketio.on('remove_lock')
def on_lock_remove(data):
    """
    In order to prevent users from working on the same puzzle piece at the same
    time, the frontend can emit "add_lock" events; this event allows events to be
    removed, but routing the remove event to all members of the current room.
    """
    if 'puzzle_id' not in data.keys():
        return

    print("A new lock should be removed, based on user completing their submission.")
    socketio.emit('lock_update_remove', data, room=int(data['puzzle_id']))


@socketio.on('leave')
def on_leave(data):
    """
    Called upon when a client emits an event to leave a puzzle room.
    Expects that data should be in format {puzzle_id: <puzzle_id>}.
    """
    if 'puzzle_id' not in data.keys():
        return

    puzzle_id = int(data['puzzle_id'])
    leave_room(puzzle_id)
    socketio.emit('player_left', {"msg": f'Player left room {puzzle_id}'}, room=puzzle_id)
    print(rooms())
