from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

# create a new puzzle

# add new users to a puzzle

# add a new value to the puzzle

# return all puzzles for a user

# return a specific puzzle for a user

# return leaderboard scores


class Sudoku(Resource):

    @jwt_required
    def get(self):
        """
        Returns the Sudoku Puzzle, including all players and all moves made on gameboard
        """

        # find the puzzles for the user; if the p

        return {
            'users': True
        }


class PuzzlePieces(Resource):

    @jwt_required
    def post(self):
        """
        Finds all moves made on puzzle.
        """
        return {
            'sudoku': True
        }

