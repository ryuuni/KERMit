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
from flask_cors import CORS
from flask import Flask, request, make_response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, leave_room, send, emit

# ------  Set Configuration Settings ---------

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

#  ------- Configure CORS ------------

# setup extension for handling Cross Origin Resource Sharing
cors = CORS(app)


@app.before_request
def handle_cors():
    """
    Approach to handle Cross Origin Resource Sharing; this approach
    allows requests for all origins. This approach was used after
    failure to get CORS(app) approach to work with React. Inspiration
    for this approach from Niels B on StackOverflow at
    https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
    """
    def _build_cors_prelight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()


# -------- Setup Database ------------

db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    """
    Creates all database tables relevant to this application,
    if the tables do not already exist, before the first request is handed
    """
    db.create_all()


# ------- Allow socket capabilities -------
# setup socketio for handling web sockets
socketio = SocketIO(app, manage_session=True)


@socketio.on('join')
def on_join(data):
    """
    Leave a websocket representing a puzzle room; data should be in
    format {puzzle_id: <puzzle_id>}, where puzzle_id represents a "room" that can be
    joined.
    """
    puzzle_id = data['puzzle_id']
    join_room(room=puzzle_id)
    socketio.emit('left', {"msg": f'Player joined room {puzzle_id}'}, room=puzzle_id)


@socketio.on('leave')
def on_leave(data):
    """
    Leave a websocket representing a puzzle room
    """
    puzzle_id = data['puzzle_id']
    leave_room(puzzle_id)
    socketio.emit('left', {"msg": f'Player left room {puzzle_id}'}, room=puzzle_id)


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

if __name__ == '__main__':
    socketio.run(app)
