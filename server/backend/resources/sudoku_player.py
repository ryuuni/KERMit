"""
Resource for adding a new player to a puzzle that already exists.
"""
from flask import g
from flask_restful import Resource
from backend.models.player import PuzzlePlayer
from backend.models.puzzle_exception import PuzzleException


class SudokuPlayer(Resource):
    """
    Resource for adding a new player to a puzzle.
    """

    @staticmethod
    def post(puzzle_id):
        """
        Player may add themselves to the puzzle, if they are not already affiliated with
        the puzzle.
        """
        # find all puzzles associated with the player making the request
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g.user.g_id)

        # if the requested puzzle doesn't exist for the user, then return error
        if any(puzzle.puzzle_id == puzzle_id for puzzle in player_puzzles):
            return {
                'message': f"{g.user.as_str()} is already is associated "
                           f"with puzzle {puzzle_id}."
            }

        # try to add the user to the puzzle
        try:
            PuzzlePlayer.add_player_to_puzzle(puzzle_id, g.user)

            # send back successful message
            return {
                'message': f"Successfully added {g.user.as_str()} to "
                           f"puzzle with id {puzzle_id}."
            }

        except PuzzleException as p_exception:
            return {'message': f"Attempt to add {g.user.as_str()} to puzzle {puzzle_id} failed.",
                    'reason': p_exception.get_message()}, 400

        except Exception as exception:  # pylint: disable=broad-except
            print(f"{exception}")
            return {'message': f"Attempt to add {g.user.as_str()} to puzzle {puzzle_id} failed.",
                    'reason': 'Unknown error occurred.'}, 500
