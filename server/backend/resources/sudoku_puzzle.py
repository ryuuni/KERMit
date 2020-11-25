"""
Resource for getting a puzzle by ID and editing a puzzle (i.e, adding players).
"""
from flask import g
from flask_restful import Resource
from backend.models.player import PuzzlePlayer
from backend.models.puzzle_exception import PuzzleException
from backend.models.sudoku_puzzle import Puzzle


class SudokuPuzzle(Resource):
    """
    Resource for creating and retrieving Sudoku puzzles.
    """

    @staticmethod
    def get(puzzle_id):
        """
        Finds a puzzle specified by puzzle_id.
        """
        # find all puzzles associated with the player making the request
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g.user.g_id)

        # if the requested puzzle doesn't exist for the user, then return error
        if not any(puzzle.puzzle_id == puzzle_id for puzzle in player_puzzles):
            return {'message': f"Puzzle requested does not exist or is not associated "
                               f"with user {g.user.as_str()}"}, 404  # not found

        # get the puzzle and return it back
        return sudoku_to_dict(
            puzzle=Puzzle.get_puzzle(puzzle_id),
            puzzle_players=PuzzlePlayer.find_players_for_puzzle(puzzle_id)
        )

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


def sudoku_to_dict(puzzle, puzzle_players=None):
    """
    Converts information about a Sudoku board into a dictionary.
    """

    def puzzle_piece_as_dict(puzzle_piece):
        """ Helper function for converting puzzle pieces to dictionaries"""
        return {
            'x_coordinate': puzzle_piece.x_coordinate,
            'y_coordinate': puzzle_piece.y_coordinate,
            'static_piece': puzzle_piece.static_piece,
            'value': puzzle_piece.value
        }

    def user_as_dict(user):
        """Helper function for converting a user into a dictionary"""
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

    puzzle = {
        'puzzle_id': puzzle.id,
        'completed': puzzle.completed,
        'difficulty': puzzle.difficulty,
        'point_value': puzzle.point_value,
        'pieces': [puzzle_piece_as_dict(piece) for piece in puzzle.puzzle_pieces]
    }

    # puzzle players do not have to be specified
    if puzzle_players:
        puzzle['players'] = [user_as_dict(player) for player in puzzle_players]

    return puzzle
