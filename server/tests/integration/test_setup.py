from server.server import app, db
from server.config import IntegrationTestingConfig
from server.models.user import User
from server.models.sudoku_puzzle import Puzzle
from server.models.player import PuzzlePlayer
import pytest
import os


@pytest.fixture(scope='module')
def test_client():

    app.config.from_object(IntegrationTestingConfig)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    print(f"OS set to {os.getenv('SQLALCHEMY_DATABASE_URI_TEST')}")

    # create a test client using testing configurations
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_db(test_client):

    # setup -- create the database tables
    db.create_all()
    db.session.commit()

    # create a bunch of test users
    integration_tester = User('integration_tester', 'test_test')  # user with id = 1
    integration_tester.save()
    foobar = User('foobar', 'really_secure_password')             # user with id = 2
    foobar.save()
    princess = User('PrincessPea', 'crown')                       # user with id = 3
    princess.save()
    trump = User('DonaldTrump', 'drumpy')                         # user with id = 4
    trump.save()
    biden = User('JoeBiden', 'biden2020')                         # user with id = 5
    biden.save()

    # save two puzzles, both associated with user foobar (user_id = 2)
    sudoku = Puzzle(difficulty_level=0.6, size=4)   # puzzle with id = 1
    sudoku.save(autocommit=True)
    sudoku = Puzzle(difficulty_level=0.3, size=3)   # puzzle with id = 2
    sudoku.save(autocommit=True)

    puzzle_player = PuzzlePlayer(2, 1)
    puzzle_player.save(autocommit=True)
    puzzle_player = PuzzlePlayer(2, 2)
    puzzle_player.save(autocommit=True)

    yield db  # run the actual tests

    # tear down -- drop the database tables
    db.session.remove()
    db.drop_all()

