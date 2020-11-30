"""
Resource for getting a puzzle by ID and editing a puzzle (i.e, adding players).
"""
from flask import g
from flask_restful import Resource, reqparse, inputs
from backend.models.player import PuzzlePlayer
from backend.models.sudoku_puzzle import Puzzle


class SudokuPuzzle(Resource):
    """
    Resource for creating and retrieving Sudoku puzzles.
    """
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)

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

    def post(self, puzzle_id):
        """
        Allows changes to be made to puzzles, namely making a specific puzzle
        hidden from a specific user in the UI.
        """
        # find all puzzles associated with the player making the request (visible and hidden)
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g_id=g.user.g_id)

        # if the requested puzzle doesn't exist for the user, then return error
        puzzle_to_edit = None
        for puzzle in player_puzzles:
            if puzzle.puzzle_id == puzzle_id:
                puzzle_to_edit = puzzle

        if not puzzle_to_edit:
            return {'message': f"Puzzle requested does not exist or is not associated "
                               f"with user {g.user.as_str()}"}, 404  # not found

        # parse the visibility
        self.parser.add_argument('hidden', type=inputs.boolean, required=True,
                                 help='Set the visibility of the puzzle for a specific user; '
                                      'True will set the puzzle as hidden.')
        args = self.parser.parse_args()
        try:
            puzzle_to_edit.update_visibility(args['hidden'])

            # send back successful message
            return {
                'message': f"Successfully updated the visibility of puzzle "
                           f"{puzzle_to_edit.puzzle_id} for player {g.user.id} "
                           f"to hidden = {args['hidden']}"
            }

        except Exception as exception:  # pylint: disable=broad-except
            print(f"{exception}")
            return {'message': "Attempt to edit the visibility of puzzle failed",
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
