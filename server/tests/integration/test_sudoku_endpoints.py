import pytest
from server.tests.integration.test_setup import test_client, init_db


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
    assert response.json == {'message': 'No sudoku puzzles are associated with this account'}


def test_get_nonexistent_puzzle(test_client, init_db):
    response = test_client.get('/puzzles/2')
    assert response.status_code == 404
    assert response.json == {
        'message': f"Puzzle requested does not exist or is not associated with user 'integration_tester'."
    }


def test_save_new_puzzle_valid(test_client, init_db):
    response = test_client.post('/puzzles', data=dict(difficulty=0.5, size=3))
    assert response.status_code == 200
    assert response.json == {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 3,
        'puzzle_id': 2
    }


def test_save_new_puzzle_invalid_difficulty_small(test_client, init_db):
    """
    Test create a puzzle of invalid difficulty
    """
    response = test_client.post('/puzzles', data=dict(difficulty=1.1, size=3))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Difficulty levels must range between 0.01 and 0.99. Got 1.1.'
    }


def test_save_new_puzzle_invalid_difficulty_large(test_client, init_db):
    """
    Test create a puzzle of invalid difficulty
    """
    response = test_client.post('/puzzles', data=dict(difficulty=0.0, size=3))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Difficulty levels must range between 0.01 and 0.99. Got 0.0.'
    }


def test_save_new_puzzle_invalid_size_large(test_client, init_db):
    """
    Test create a puzzle of invalid difficulty
    """
    response = test_client.post('/puzzles', data=dict(difficulty=0.5, size=10))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Valid sizes range from 2 to 5. Got 10.'
    }


def test_save_new_puzzle_invalid_size_small(test_client, init_db):
    """
    Test create a puzzle of invalid difficulty
    """
    response = test_client.post('/puzzles', data=dict(difficulty=0.5, size=1))
    assert response.status_code == 400
    assert response.json == {
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Valid sizes range from 2 to 5. Got 1.'
    }


def test_get_all_puzzles_for_user(test_client, init_db):
    response = test_client.get('/puzzles')
    expected = {
        'puzzles':
        [
            {
                'puzzle_id': 2,
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
    response = test_client.get('/puzzles/2')
    expected = {
        'puzzle_id': 2,
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


