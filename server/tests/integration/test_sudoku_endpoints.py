import pytest
from server.tests.integration.test_setup import test_client, init_db


@pytest.fixture(scope="function", autouse=True)
def no_jwt(monkeypatch):
    """Monkeypatch the JWT verification functions for tests"""
    monkeypatch.setattr("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda: 'integration_tester')


@pytest.fixture(scope="function", autouse=True)
def user(monkeypatch):
    def mock_username(*args, **kwargs):
        return 'integration_tester'

    monkeypatch.setattr('server.resources.sudoku.get_request_username', mock_username)


def test_save_new_puzzle_difficulty_not_specified(test_client, init_db):
    response = test_client.post('/puzzles')
    assert response.status_code == 400
    assert response.json['message'] == {
        'difficulty': 'The difficulty of the puzzle must be specified',
        'size': 'The size of the puzzle must be specified'
    }


def test_save_new_puzzle_valid(test_client, init_db):
    response = test_client.post('/puzzles', data=dict(difficulty=0.5, size=3))
    assert response.status_code == 200
    assert response.json == {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 3,
        'puzzle_id': 1
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
    assert response.status_code == 200
    assert response.json == [{'puzzle_id': 1, 'completed': False, 'difficulty': 0.5, 'point_value': 90,
                              'pieces': [{'x_coordinate': 0, 'y_coordinate': 0, 'static_piece': True, 'value': 5},
                                         {'x_coordinate': 0, 'y_coordinate': 1, 'static_piece': True, 'value': 1},
                                         {'x_coordinate': 0, 'y_coordinate': 2, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 0, 'y_coordinate': 3, 'static_piece': True, 'value': 6},
                                         {'x_coordinate': 0, 'y_coordinate': 4, 'static_piece': True, 'value': 9},
                                         {'x_coordinate': 0, 'y_coordinate': 5, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 0, 'y_coordinate': 6, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 0, 'y_coordinate': 7, 'static_piece': True, 'value': 2},
                                         {'x_coordinate': 0, 'y_coordinate': 8, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 1, 'y_coordinate': 0, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 1, 'y_coordinate': 1, 'static_piece': True, 'value': 2},
                                         {'x_coordinate': 1, 'y_coordinate': 2, 'static_piece': True, 'value': 7},
                                         {'x_coordinate': 1, 'y_coordinate': 3, 'static_piece': True, 'value': 1},
                                         {'x_coordinate': 1, 'y_coordinate': 4, 'static_piece': True, 'value': 4},
                                         {'x_coordinate': 1, 'y_coordinate': 5, 'static_piece': True, 'value': 8},
                                         {'x_coordinate': 1, 'y_coordinate': 6, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 1, 'y_coordinate': 7, 'static_piece': True, 'value': 9},
                                         {'x_coordinate': 1, 'y_coordinate': 8, 'static_piece': True, 'value': 3},
                                         {'x_coordinate': 2, 'y_coordinate': 0, 'static_piece': True, 'value': 4},
                                         {'x_coordinate': 2, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 2, 'y_coordinate': 2, 'static_piece': True, 'value': 9},
                                         {'x_coordinate': 2, 'y_coordinate': 3, 'static_piece': True, 'value': 3},
                                         {'x_coordinate': 2, 'y_coordinate': 4, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 2, 'y_coordinate': 5, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 2, 'y_coordinate': 6, 'static_piece': True, 'value': 1},
                                         {'x_coordinate': 2, 'y_coordinate': 7, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 2, 'y_coordinate': 8, 'static_piece': True, 'value': 7},
                                         {'x_coordinate': 3, 'y_coordinate': 0, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 3, 'y_coordinate': 1, 'static_piece': True, 'value': 7},
                                         {'x_coordinate': 3, 'y_coordinate': 2, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 3, 'y_coordinate': 3, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 3, 'y_coordinate': 4, 'static_piece': True, 'value': 3},
                                         {'x_coordinate': 3, 'y_coordinate': 5, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 3, 'y_coordinate': 6, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 3, 'y_coordinate': 7, 'static_piece': True, 'value': 1},
                                         {'x_coordinate': 3, 'y_coordinate': 8, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 4, 'y_coordinate': 0, 'static_piece': True, 'value': 1},
                                         {'x_coordinate': 4, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 4, 'y_coordinate': 2, 'static_piece': True, 'value': 2},
                                         {'x_coordinate': 4, 'y_coordinate': 3, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 4, 'y_coordinate': 4, 'static_piece': True, 'value': 8},
                                         {'x_coordinate': 4, 'y_coordinate': 5, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 4, 'y_coordinate': 6, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 4, 'y_coordinate': 7, 'static_piece': True, 'value': 3},
                                         {'x_coordinate': 4, 'y_coordinate': 8, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 5, 'y_coordinate': 0, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 5, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 5, 'y_coordinate': 2, 'static_piece': True, 'value': 6},
                                         {'x_coordinate': 5, 'y_coordinate': 3, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 5, 'y_coordinate': 4, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 5, 'y_coordinate': 5, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 5, 'y_coordinate': 6, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 5, 'y_coordinate': 7, 'static_piece': True, 'value': 4},
                                         {'x_coordinate': 5, 'y_coordinate': 8, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 6, 'y_coordinate': 0, 'static_piece': True, 'value': 2},
                                         {'x_coordinate': 6, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 6, 'y_coordinate': 2, 'static_piece': True, 'value': 5},
                                         {'x_coordinate': 6, 'y_coordinate': 3, 'static_piece': True, 'value': 8},
                                         {'x_coordinate': 6, 'y_coordinate': 4, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 6, 'y_coordinate': 5, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 6, 'y_coordinate': 6, 'static_piece': True, 'value': 4},
                                         {'x_coordinate': 6, 'y_coordinate': 7, 'static_piece': True, 'value': 7},
                                         {'x_coordinate': 6, 'y_coordinate': 8, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 7, 'y_coordinate': 0, 'static_piece': True, 'value': 7},
                                         {'x_coordinate': 7, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 7, 'y_coordinate': 2, 'static_piece': True, 'value': 8},
                                         {'x_coordinate': 7, 'y_coordinate': 3, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 7, 'y_coordinate': 4, 'static_piece': True, 'value': 2},
                                         {'x_coordinate': 7, 'y_coordinate': 5, 'static_piece': True, 'value': 9},
                                         {'x_coordinate': 7, 'y_coordinate': 6, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 7, 'y_coordinate': 7, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 7, 'y_coordinate': 8, 'static_piece': True, 'value': 1},
                                         {'x_coordinate': 8, 'y_coordinate': 0, 'static_piece': True, 'value': 9},
                                         {'x_coordinate': 8, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 8, 'y_coordinate': 2, 'static_piece': True, 'value': 1},
                                         {'x_coordinate': 8, 'y_coordinate': 3, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 8, 'y_coordinate': 4, 'static_piece': True, 'value': 7},
                                         {'x_coordinate': 8, 'y_coordinate': 5, 'static_piece': True, 'value': 3},
                                         {'x_coordinate': 8, 'y_coordinate': 6, 'static_piece': False, 'value': None},
                                         {'x_coordinate': 8, 'y_coordinate': 7, 'static_piece': True, 'value': 8},
                                         {'x_coordinate': 8, 'y_coordinate': 8, 'static_piece': False, 'value': None}],
                              'players': [{'username': 'integration_tester', 'id': 1}]}]
