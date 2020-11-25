"""
TO DO
"""
from flask import make_response, request
from flask_socketio import join_room, leave_room, rooms
from backend import app, db, socketio, api
from backend.resources.authentication import Registration, _verify_token
from backend.resources.sudoku import SudokuPuzzles, SudokuPuzzle, \
    SudokuPuzzlePiece, SudokuPuzzleSolution
from backend.resources.leaderboard import Leaderboard


@app.before_first_request
def create_tables():
    """
    Creates all database tables relevant to this application,
    if the tables do not already exist, before the first request is handed
    """
    db.create_all()


@app.before_request
def handle_cors():
    """
    Approach to handle Cross Origin Resource Sharing; this approach
    allows requests for all origins. This approach was used after
    failure to get CORS(backend) simplistic approach to work with React. Instead,
    we ensure we enable access for OPTIONS pre-flight requests and returning
    approval. Inspiration for this approach from Niels B on StackOverflow at
    https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
    """
    def _build_cors_preflight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()


@app.before_request
def verify_token():
    """
    Method to run before all requests; determines if a user has a valid
    Google OAuth2 token and uses the token to discover who the user making the request is.
    The user is then loaded in from the database and stored in a special flask object called 'g'.
    While g is not appropriate for storing data across requests, it provides a global namespace
    for holding any data you want during a single backend context.
    """
    # allow the health check endpoint to be unauthenticated
    if request.endpoint is None or request.endpoint != '/':
        return None
    return _verify_token(request)


@socketio.on('connect')
def test_connect():
    print(f"Client with unique session ID {request.sid} has connected...")
    socketio.emit('connection', {'msg': 'Client connected'})


@socketio.on('disconnect')
def test_disconnect():
    print(f'Client has been disconnected')


@socketio.on('join')
def on_join(data):
    """
    Leave a websocket representing a puzzle room; data should be in
    format {puzzle_id: <puzzle_id>}, where puzzle_id represents a "room" that can be
    joined.
    """
    print("This is the data received: " + str(data))
    puzzle_id = data['puzzle_id']
    join_room(room=puzzle_id)
    socketio.emit('left', {"msg": f'Player joined room {puzzle_id}'}, room=puzzle_id)
    print("These are the rooms for user: " + str(rooms()))


@socketio.on('leave')
def on_leave(data):
    """
    Leave a websocket representing a puzzle room
    """
    print(data)
    puzzle_id = data['puzzle_id']
    leave_room(puzzle_id)
    socketio.emit('left', {"msg": f'Player left room {puzzle_id}'}, room=puzzle_id)
    print(rooms())


@socketio.on_error_default
def default_error_handler(exception):
    print(exception)


# --------------- Register HTTP endpoints and callbacks for API ----------


@app.route('/')
def health_check():
    return {'msg': 'Hello! Application is OK!'}


api.add_resource(Registration, '/register')
api.add_resource(SudokuPuzzles, '/puzzles')
api.add_resource(SudokuPuzzle, '/puzzles/<int:puzzle_id>')
api.add_resource(SudokuPuzzleSolution, '/puzzles/<int:puzzle_id>/solution')
api.add_resource(SudokuPuzzlePiece, '/puzzles/<int:puzzle_id>/piece')
api.add_resource(Leaderboard, '/leaderboard')
