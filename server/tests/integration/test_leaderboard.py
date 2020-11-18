"""
Integration tests for leaderboard endpoints
"""
from server.server import app  # prevent circular imports
from server.models.player import PuzzlePlayer
from server.models.sudoku_puzzle import Puzzle
from server.tests.integration.test_setup import test_client, init_db
from server.tests.integration.integration_mocks import verification_true


def test_get_leaders_no_completed_puzzle(test_client, init_db, verification_true):
    """
    Test the response when user makes request for leaderboard when there
    is no one on the leaderboard.
    """
    response = test_client.get('/leaderboard', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 200
    assert response.json == {'players': []}


def test_get_leaders_completed_puzzles(test_client, init_db, verification_true):
    """
    Test the response when a valid request is made for a top leaderboard players.
    """

    # create a completed puzzle, then add some players to it
    sudoku = Puzzle(difficulty_level=0.4, size=2)   # puzzle with id = 3
    sudoku.completed = True
    sudoku.save(autocommit=True)

    puzzle_player = PuzzlePlayer(2, 3)
    puzzle_player.save(autocommit=True)
    puzzle_player = PuzzlePlayer(1, 3)
    puzzle_player.save(autocommit=True)

    response = test_client.get('/leaderboard', headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 200
    assert response.json == {
        'players': [{'first_name': 'foo', 'last_name': 'bar', 'score': 45},
                    {'first_name': 'integration', 'last_name': 'tester', 'score': 45}]
    }


def test_get_leaders_completed_puzzles_limit2(test_client, init_db, verification_true):
    """
    Test the response when a valid request is made for a top leaderboard players, the limit
    on players is provided.

    Important: This test relies on the test_get_leaders_completed_puzzles()
    test to complete, meaning that the ordering is important.
    """
    response = test_client.get('/leaderboard',
                               query_string={'limit': '2'},
                               headers={'Authorization': 'Bearer 2342351231asdb'})
    assert response.status_code == 200
    assert response.json == {
        'players': [{'first_name': 'foo', 'last_name': 'bar', 'score': 45},
                    {'first_name': 'integration', 'last_name': 'tester', 'score': 45}]
    }
