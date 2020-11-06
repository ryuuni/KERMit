from server.server import app, db
from server.models.sudoku_puzzle import Puzzle
from server.models.user import User
from server.resources.sudoku import sudoku_to_dict
from server.config import UnitTestingConfig

app.config.from_object(UnitTestingConfig)
db = None


def test_sudoku_to_json():
    foobar = User('54321', 'foo', 'bar', 'foobar@comsci.com')
    foobar.id = 1

    princess = User('98734', 'Princess', 'Bride', 'princess@princessbride.com')
    princess.id = 2

    sudoku = Puzzle(difficulty_level=0.6, size=4)
    players = [foobar, princess]

    result = sudoku_to_dict(sudoku, players)

    # note that because you cannot predict what sudoku boards are created, not comparing pieces,
    # just for simplicity for now
    assert not result['puzzle_id']
    assert not result['completed']
    assert result['difficulty'] == 0.6
    assert result['point_value'] == 110
    assert result['players'] == [
        {'id': 1, 'first_name': 'foo', 'last_name': 'bar', 'email': 'foobar@comsci.com'},
        {'id': 2, 'first_name': 'Princess', 'last_name': 'Bride', 'email': 'princess@princessbride.com'}
    ]
