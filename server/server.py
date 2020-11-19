"""
Main file for configuration of Flask application. Responsible for configuration of
settings, based on environmental variables, and setting up the database before the
first request.

NOTE: Usually imports are made at top of file; however these must be imported after
app is created in order to register properly. Also note that these imports do not need to
be used, explicitly, they just need to be imported. This funky Flask configuration
causes style errors, but it is not a problem, so they have been commented out with
# pylint: disable=wrong-import-position
"""
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# ------  Set Configuration Settings ---------

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# -------- Setup Database ------------

db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    """
    Creates all database tables relevant to this application,
    if the tables do not already exist, before the first request is handed
    """
    db.create_all()


# ----- Register endpoints and callbacks -------

from server.resources.authentication import Registration   # pylint: disable=wrong-import-position
from server.resources.sudoku import SudokuPuzzles, SudokuPuzzle, \
    SudokuPuzzlePiece, SudokuPuzzleSolution  # pylint: disable=wrong-import-position
from server.resources.leaderboard import Leaderboard  # pylint: disable=wrong-import-position

api = Api(app)
api.add_resource(Registration, '/register')
api.add_resource(SudokuPuzzles, '/puzzles')
api.add_resource(SudokuPuzzle, '/puzzles/<int:puzzle_id>')
api.add_resource(SudokuPuzzleSolution, '/puzzles/<int:puzzle_id>/solution')
api.add_resource(SudokuPuzzlePiece, '/puzzles/<int:puzzle_id>/piece')
api.add_resource(Leaderboard, '/leaderboard')
