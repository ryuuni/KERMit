import pytest

from server.server import db, app
from server.models.player import PuzzlePlayer
from server.models.puzzle_pieces import PuzzlePiece
from server.tests.integration.test_setup import test_client, init_db
from server.models.user import User


@pytest.fixture(scope="function", autouse=True)
def no_jwt(monkeypatch):
    """Monkeypatch the JWT verification functions for tests"""
    monkeypatch.setattr("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda: 'integration_tester')


@pytest.fixture(scope="function", autouse=True)
def user(monkeypatch):
    """Monkeypatch for the username of the requesting person, without JWT verification"""
    def mock_username(*args, **kwargs):
        return 'integration_tester'

    monkeypatch.setattr('server.resources.sudoku.get_request_username', mock_username)


def test_get_all_puzzles_no_puzzles(test_client, init_db):
    """
    Test the response when the user makes a request to get their puzzles, but they don't have any.
    """
    response = test_client.get('/puzzles')
    assert response.status_code == 200
    assert response.json == {
        'message': 'No sudoku puzzles are associated with this account',
        'puzzles': []
    }


def test_get_nonexistent_puzzle(test_client, init_db):
    """
    Test the response when a user makes a request for a puzzle that doesn't exist.
    """
    response = test_client.get('/puzzles/10')
    assert response.status_code == 404
    assert response.json == {
        'message': f"Puzzle requested does not exist or is not associated with user 'integration_tester'."
    }


def test_save_new_puzzle_valid(test_client, init_db):
    """
    Test the response when a user makes a valid request to create a new sudoku puzzle
    """
    response = test_client.post('/puzzles', data=dict(difficulty=0.5, size=3))
    assert response.status_code == 200
    assert response.json == {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 3,
        'puzzle_id': 3
    }


def test_save_new_puzzle_invalid_difficulty_small(test_client, init_db):
    """
    Test the response when a user makes a request to create a puzzle of invalid difficulty (too high).
    """
    response = test_client.post('/puzzles', data=dict(difficulty=1.1, size=3))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Difficulty levels must range between 0.01 and 0.99. Got 1.1.'
    }


def test_save_new_puzzle_invalid_difficulty_large(test_client, init_db):
    """
    Test the response when a user makes a request to create a puzzle of invalid difficulty (too low).
    """
    response = test_client.post('/puzzles', data=dict(difficulty=0.0, size=3))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Difficulty levels must range between 0.01 and 0.99. Got 0.0.'
    }


def test_save_new_puzzle_invalid_size_large(test_client, init_db):
    """
    Test the response when a user makes a request to create a puzzle of invalid size (too large).
    """
    response = test_client.post('/puzzles', data=dict(difficulty=0.5, size=10))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Valid sizes range from 2 to 5. Got 10.'
    }


def test_save_new_puzzle_invalid_size_small(test_client, init_db):
    """
    Test the response when a user makes a request to create a puzzle of invalid size (too small).
    """
    response = test_client.post('/puzzles', data=dict(difficulty=0.5, size=1))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Valid sizes range from 2 to 5. Got 1.'
    }


def test_get_all_puzzles_for_user(test_client, init_db):
    """
    Test response for valid request to get all puzzzles associated with user.
    """
    response = test_client.get('/puzzles')
    expected = {
        'puzzles':
        [
            {
                'puzzle_id': 3,
                'completed': False,
                'difficulty': 0.5,
                'point_value': 90,
                'pieces': ["this would ordinarily contain a list of pieces; they're not predictable in tests"],
                'players': [{'username': 'integration_tester', 'id': 1}]
            }
        ]
    }

    # cannot test for pieces easily; this is randomly created by the Sudoku library for each round
    response.json['puzzles'][0].pop('pieces')
    expected['puzzles'][0].pop('pieces')

    assert response.status_code == 200
    assert response.json == expected


def test_get_puzzle_valid(test_client, init_db):
    """
    An attempt to get a puzzle with a valid id that is associated with the requesting user should
    be successful.
    """
    response = test_client.get('/puzzles/3')
    expected = {
        'puzzle_id': 3,
        'completed': False,
        'difficulty': 0.5,
        'point_value': 90,
        'pieces': ["this would ordinarily contain a list of pieces; they're not predictable in tests"],
        'players': [{'username': 'integration_tester', 'id': 1}]
    }

    # cannot test for pieces easily; this is randomly created by the Sudoku library for each round
    response.json.pop('pieces')
    expected.pop('pieces')

    assert response.status_code == 200
    assert response.json == expected


def test_attempt_to_get_unaffiliated_puzzle(test_client, init_db):
    """
    An attempting to get a puzzle with a valid id, but that is not associated with the requesting
    user should not return the puzzle.
    """
    response = test_client.get('/puzzles/1')
    assert response.status_code == 404
    assert response.json == {
            'message': f"Puzzle requested does not exist or is not "
                       f"associated with user 'integration_tester'."
    }


def test_attempt_to_add_player_to_puzzle_already_in_puzzle(test_client, init_db):
    """
    Attempt to add player that is already in the puzzle should not re-add the player.
    """
    response = test_client.post('/puzzles/3')
    assert response.status_code == 200
    assert response.json == {'message': "User 'integration_tester' already is associated with puzzle 3."}


def test_attempt_to_add_player_to_puzzle_that_doesnt_exist(test_client, init_db):
    """
    Attempt by a player to add themselves to a puzzle that doesn't exist should not be successful.
    """
    response = test_client.post('/puzzles/10')
    assert response.status_code == 400
    assert response.json == {
        'message': "Attempt to add user 'integration_tester' to puzzle 10 failed.",
        'reason': 'You cannot join a puzzle if the puzzle does not exist and have at least 1 player.'
    }


def test_attempt_to_add_player_to_puzzle_valid(test_client, init_db):
    """
    Attempt to add player to puzzle that is a valid request should be successful
    """
    response = test_client.post('/puzzles/1')
    assert response.status_code == 200
    assert response.json == {'message': "Successfully added user 'integration_tester' to puzzle with id 1."}


def test_attempt_to_join_puzzle_max_players_reached(test_client, init_db):
    """
    Attempt to add player to puzzle that is a valid request should be successful.
    """
    # add three more players to puzzle with id = 2; now the board has 4 players
    puzzle_player = PuzzlePlayer(3, 2)
    puzzle_player.save(autocommit=True)
    puzzle_player = PuzzlePlayer(4, 2)
    puzzle_player.save(autocommit=True)
    puzzle_player = PuzzlePlayer(5, 2)
    puzzle_player.save(autocommit=True)

    response = test_client.post('/puzzles/2')
    assert response.status_code == 400
    assert response.json == {
        'message': "Attempt to add user 'integration_tester' to puzzle 2 failed.",
        'reason': 'There are already 4 players affiliated with puzzle 2'
    }


def test_attempt_add_piece_valid_no_value_yet(test_client, init_db):
    """
    Attempt to add a valid number to a valid position on a sudoku board that is associated with the user.
    """
    # make sure that we know what the status is of the piece that we are attempting to change
    piece = PuzzlePiece.get_piece(3, 0, 0)
    piece.static_piece = False
    piece.value = None
    piece.save(autocommit=True)

    response = test_client.post(
        '/puzzles/3/piece', data=dict(
            x_coordinate=0,
            y_coordinate=0,
            value=2
        )
    )
    assert response.status_code == 200
    assert response.json == {
        'message': 'Successfully saved the submission of 2 at (0, 0) on puzzle_id 3 '
                   'by user \'integration_tester\''
    }

    # test that database is updated
    piece = PuzzlePiece.get_piece(3, 0, 0)
    assert piece.value == 2


def test_attempt_add_piece_valid_override_value(test_client, init_db):
    """
    Attempt to add a valid number to a valid position on a sudoku board that is associated with the user.
    """
    # make sure that we know what the status is of the piece that we are attempting to change
    piece = PuzzlePiece.get_piece(3, 0, 0)
    piece.static_piece = False
    piece.value = 8
    piece.save(autocommit=True)

    response = test_client.post(
        '/puzzles/3/piece', data=dict(
            x_coordinate=0,
            y_coordinate=0,
            value=2
        )
    )

    assert response.status_code == 200
    assert response.json == {
        'message': 'Successfully saved the submission of 2 at (0, 0) on puzzle_id 3 '
                   'by user \'integration_tester\''
    }

    # test that database is updated
    piece = PuzzlePiece.get_piece(3, 0, 0)
    assert piece.value == 2


def test_attempt_add_piece_puzzle_player_is_not_affiliated_with(test_client, init_db):
    """
    Attempt to add a valid number to a valid position on a sudoku board that is NOT associated with the user.
    """
    response = test_client.post(
        '/puzzles/2/piece', data=dict(
            x_coordinate=0,
            y_coordinate=0,
            value=2
        )
    )
    assert response.status_code == 404
    assert response.json == {
        'message': 'Puzzle requested does not exist '
                   'or is not associated with this Player.'
    }


def test_attempt_add_piece_invalid_piece_low(test_client, init_db):
    """
    Attempt to add a INVALID number to a valid position on a sudoku board that is associated with the user.
    """
    piece = PuzzlePiece.get_piece(3, 0, 0)
    piece.static_piece = False
    piece.value = None
    piece.save(autocommit=True)

    response = test_client.post(
        '/puzzles/3/piece', data=dict(
            x_coordinate=0,
            y_coordinate=0,
            value=50
        )
    )
    assert response.status_code == 400
    assert response.json == {
        'message': 'Attempt to save 50 at (0, 0) on puzzle_id 3 by user '
                   'integration_tester was unsuccessful',
        'reason': 'Invalid value provided (50). the range of the puzzle. '
                  'Available values are 1 to 9.'
    }


def test_attempt_add_piece_invalid_piece_high(test_client, init_db):
    """
    Attempt to add a INVALID number to a valid position on a sudoku board that is associated with the user.
    """
    piece = PuzzlePiece.get_piece(3, 0, 0)
    piece.static_piece = False
    piece.value = None
    piece.save(autocommit=True)

    response = test_client.post(
        '/puzzles/3/piece', data=dict(
            x_coordinate=0,
            y_coordinate=0,
            value=0
        )
    )
    assert response.status_code == 400
    assert response.json == {
        'message': 'Attempt to save 0 at (0, 0) on puzzle_id 3 by user '
                   'integration_tester was unsuccessful',
        'reason': 'Invalid value provided (0). the range of the puzzle. '
                  'Available values are 1 to 9.'
    }


def test_attempt_add_piece_invalid_position_high(test_client, init_db):
    """
    Attempt to add a valid number to an INVALID position on a sudoku board that is associated with the user.
    """
    response = test_client.post(
        '/puzzles/3/piece', data=dict(
            x_coordinate=100,
            y_coordinate=100,
            value=2
        )
    )
    assert response.status_code == 400
    assert response.json == {
        'message': 'Attempt to save 2 at (100, 100) on puzzle_id 3 by user '
                   'integration_tester was unsuccessful',
        'reason': 'Coordinates provided (100, 100) are outside the range of the puzzle. '
                  'Available coordinates are (0, 0) to (9, 9).'
    }


def test_attempt_add_piece_invalid_position_low(test_client, init_db):
    """
    Attempt to add a valid number to an INVALID position on a sudoku board that is associated with the user.
    """
    response = test_client.post(
        '/puzzles/3/piece', data=dict(
            x_coordinate=-1,
            y_coordinate=-10,
            value=2
        )
    )
    assert response.status_code == 400
    assert response.json == {
        'message': 'Attempt to save 2 at (-1, -1) on puzzle_id 3 by user '
                   'integration_tester was unsuccessful',
        'reason': 'Coordinates provided (-1, -10) are outside the range of the puzzle. '
                  'Available coordinates are (0, 0) to (9, 9).'
    }
