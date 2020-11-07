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
    db.create_all()


# ----- Register endpoints and callbacks -------

"""
NOTE: Usually imports are made at top of file; however these must be imported after app is created in
order to register properly. Also note that these imports do not need to be used. This is sort of a weird
expectation of Flask-SQLAlchemy. Hence why # nopep8 was used here.
"""
from server.resources.authentication import Registration  # nopep8
from server.resources.sudoku import SudokuPuzzles, SudokuPuzzle, SudokuPuzzlePiece, \
    HealthCheck, SudokuPuzzleSolution  # nopep8

api = Api(app)
api.add_resource(HealthCheck, '/hello')
api.add_resource(Registration, '/register')
api.add_resource(SudokuPuzzles, '/puzzles')
api.add_resource(SudokuPuzzle, '/puzzles/<int:puzzle_id>')
api.add_resource(SudokuPuzzleSolution, '/puzzles/<int:puzzle_id>/solution')
api.add_resource(SudokuPuzzlePiece, '/puzzles/<int:puzzle_id>/piece')
