"""
Unit tests for web socket functionality.
"""
import pytest
from backend import app, socketio
from backend.models.user import User
from backend.google_auth import GoogleAuth
from tests.unit.mocks import verification_token, mock_find_by_g_id,\
    mock_no_puzzles_for_player, mock_single_puzzles_for_player,  mock_get_puzzle


@pytest.fixture
def flask_client():
    """A test client to use for each test"""
    return app.test_client()


def test_socketio_cannot_connect_without_credentials(flask_client):
    """
    Test that it is not possible to connect without credentials.
    """
    # connect to Socket.IO without being logged in
    client = socketio.test_client(app, flask_test_client=flask_client)
    assert not client.is_connected()


def test_socketio_cannot_connect_with_invalid_credentials(monkeypatch, flask_client):
    """
    Test that it is not possible to establish socket connection without valid credential.
    """
    # connect to Socket.IO without being logged in
    def mock_verify_token(*args, **kwargs):
        """Mock the verification of the token fails."""
        return {"error": "some error", "error_description": 'A bad error occurred'}

    monkeypatch.setattr(GoogleAuth, "validate_token", mock_verify_token)

    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    assert not client.is_connected()


def test_socketio_can_connect_with_valid_credentials(flask_client, verification_token):
    """
    Test that it is not possible to connect without credentials.
    """
    # connect to Socket.IO without being logged in
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    assert client.is_connected()
    assert client.get_received() == []


def test_socketio_join_missing_token(flask_client, verification_token):
    """
    Test attempt to join room, missing token.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'puzzle_id': 1})
    assert client.get_received() == []


def test_socketio_join_missing_puzzle(flask_client, verification_token):
    """
    Test attempt to join room, missing room id (i.e., puzzle id).
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X'})
    assert client.get_received() == []


def test_socketio_join_bad_token(monkeypatch, flask_client, verification_token):
    """
    Test attempt to join room, but uses a bad token.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")

    monkeypatch.setattr(GoogleAuth, "validate_token",
                        lambda x, y: {"error": "some error",
                                   "error_description": 'A bad error occurred'})

    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    assert client.get_received() == []


def test_socketio_join_user_doesnt_exist(monkeypatch, flask_client, verification_token):
    """
    Test that if an attempt is made to join a room by an unregistered user,
    the attempt fails.
    """
    monkeypatch.setattr(User, 'find_by_g_id', lambda x: None)

    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    assert client.get_received() == []


def test_socketio_join_puzzle_not_associated(flask_client, verification_token, mock_find_by_g_id,
                                             mock_no_puzzles_for_player):
    """
    Test attempt to join room, but the room that the player is attempt to join is
    not associated with them yet; the attempt should fail.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    assert client.get_received() == []


def test_socketio_join_puzzle(flask_client, verification_token, mock_find_by_g_id,
                                             mock_single_puzzles_for_player):
    """
    Test attempt to join room, information is correct.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'}
    ]


def test_socketio_disconnect(flask_client, verification_token):
    """
    Test attempt disconnect websocket should be successful.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.disconnect()
    assert not client.is_connected()


def test_socketio_handle_move_missing_puzzle_id(flask_client, verification_token):
    """
    Test re-emit move alert to members of a room; current socket is not part of
    the room.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('move', {'x_coordinate': 1, 'y_coordinate': 5})
    assert client.get_received() == []


def test_socketio_handle_move_not_in_room(flask_client, verification_token, mock_get_puzzle):
    """
    Test re-emit move alert to members of a room; current socket is not part of
    the room.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('move', {'puzzle_id': 1, 'x_coordinate': 1, 'y_coordinate': 5})
    assert client.get_received() == []


def test_socketio_handle_move_in_room(flask_client, verification_token, mock_find_by_g_id,
                                             mock_single_puzzles_for_player, mock_get_puzzle):
    """
    Test re-emit move alert to members of a room; current socket is part of room.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('move', {'puzzle_id': 1, 'x_coordinate': 1, 'y_coordinate': 5})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'},
        {'name': 'puzzle_update', 'args': [
            {
                'puzzle_id': None,
                'completed': False,
                'difficulty': 0.5,
                'point_value': 90,
                'pieces': [
                    {'x_coordinate': 0, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                    {'x_coordinate': 1, 'y_coordinate': 1, 'static_piece': True, 'value': 3}
                ]
            }
        ], 'namespace': '/'}]


def test_socketio_handle_message(flask_client, verification_token, mock_find_by_g_id,
                                             mock_single_puzzles_for_player):
    """
    Test handle a message in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('message', {
        'puzzle_id': 1, 'message': 'This is a message', 'email': 'exampleemail.com'
    })
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'},
        {'name': 'message_update', 'args': [
            {'puzzle_id': 1, 'message': 'This is a message', 'email': 'exampleemail.com'}
        ], 'namespace': '/'}
    ]


def test_socketio_handle_message_missing_puzzle_id(flask_client, verification_token,
                                                   mock_find_by_g_id,
                                                   mock_single_puzzles_for_player):
    """
    Test handle a message in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('message', {'message': 'This is a message', 'email': 'exampleemail.com'})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'}
    ]


def test_socketio_handle_add_lock(flask_client, verification_token, mock_find_by_g_id,
                                             mock_single_puzzles_for_player):
    """
    Test handle re-emitting an addlock event in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('add_lock', {'puzzle_id': 1, 'x_coordinate': 1, 'y_coordinate': 5})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'},
        {'name': 'lock_update_add', 'args': [
            {'puzzle_id': 1, 'x_coordinate': 1, 'y_coordinate': 5}
        ], 'namespace': '/'}
    ]


def test_socketio_handle_lock_missing_puzzle_id(flask_client, verification_token, mock_find_by_g_id,
                                             mock_single_puzzles_for_player):
    """
    Test handle re-emitting an addlock event in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('add_lock', {'x_coordinate': 1, 'y_coordinate': 5})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'}
    ]


def test_socketio_handle_remove_lock(flask_client, verification_token, mock_find_by_g_id,
                                             mock_single_puzzles_for_player):
    """
    Test handle re-emitting a remove lock event in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('remove_lock', {'puzzle_id': 1, 'x_coordinate': 1, 'y_coordinate': 5})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'},
        {'name': 'lock_update_remove', 'args': [
            {'puzzle_id': 1, 'x_coordinate': 1, 'y_coordinate': 5}
        ], 'namespace': '/'}
    ]


def test_socketio_handle_remove_lock_missing_puzzle_id(flask_client, verification_token,
                                                       mock_find_by_g_id,
                                                       mock_single_puzzles_for_player):
    """
    Test handle re-emitting a remove lock event in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('remove_lock', {'x_coordinate': 1, 'y_coordinate': 5})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'}
    ]


def test_socketio_handle_leave(flask_client, verification_token, mock_find_by_g_id,
                                             mock_single_puzzles_for_player):
    """
    Test handle re-emitting a remove lock event in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('leave', {'puzzle_id': 1, 'x_coordinate': 1, 'y_coordinate': 5})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'}
    ]


def test_socketio_handle_leave_missing_puzzle_id(flask_client, verification_token,
                                                 mock_find_by_g_id, mock_single_puzzles_for_player):
    """
    Test handle re-emitting a remove lock event in a room that the current websocket is in.
    """
    client = socketio.test_client(app, flask_test_client=flask_client, query_string="?auth=X")
    client.emit('join', {'token': 'X', 'puzzle_id': 1})
    client.emit('leave', {'x_coordinate': 1, 'y_coordinate': 5})
    recvd = client.get_received()
    assert recvd == [
        {'name': 'player_joined', 'args': [{'msg': 'Player joined room 1'}], 'namespace': '/'}
    ]
