"""
Holds the definition of all the routes used in for HTTP requests
of the server
"""
from backend import app, api
from backend.resources.authentication import Registration
from backend.resources.sudoku import SudokuPuzzles, SudokuPuzzle, \
    SudokuPuzzlePiece, SudokuPuzzleSolution
from backend.resources.leaderboard import Leaderboard


@app.route('/')
def health_check():
    """
    Simple default route to provide a health check for the application
    """
    return {'msg': 'Hello! Application is OK!'}


api.add_resource(Registration, '/register')
api.add_resource(SudokuPuzzles, '/puzzles')
api.add_resource(SudokuPuzzle, '/puzzles/<int:puzzle_id>')
api.add_resource(SudokuPuzzleSolution, '/puzzles/<int:puzzle_id>/solution')
api.add_resource(SudokuPuzzlePiece, '/puzzles/<int:puzzle_id>/piece')
api.add_resource(Leaderboard, '/leaderboard')
