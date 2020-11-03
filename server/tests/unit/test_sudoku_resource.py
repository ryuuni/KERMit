from server.server import app, db
from server.models.puzzle_pieces import PuzzlePiece
from server.models.sudoku_puzzle import Puzzle
from server.models.user import User
from server.resources.sudoku import sudoku_to_dict


def test_sudoku_to_json():
    user1 = User(username='tester1', password='fake_pass1')
    user1.id = 1

    user2 = User(username='tester2', password='fake_pass2')
    user2.id = 2

    sudoku = Puzzle(difficulty_level=0.6, size=4)
    players = [user1, user2]

    result = sudoku_to_dict(sudoku, players)

    # note that because you cannot predict what sudoku boards are created, not comparing pieces,
    # just for simplicity for now
    assert not result['puzzle_id']
    assert not result['completed']
    assert result['difficulty'] == 0.6
    assert result['point_value'] == 110
    assert result['players'] == [{'username': 'tester1', 'id': 1}, {'username': 'tester2', 'id': 2}]
