"""
Resource for handling edits to individual puzzle pieces.
"""
from flask import g
from flask_restful import Resource, reqparse

from backend import socketio
from backend.models.player import PuzzlePlayer
from backend.models.puzzle_exception import PuzzleException
from backend.models.sudoku_puzzle import Puzzle
from backend.resources.sudoku_puzzle import sudoku_to_dict


class SudokuPuzzlePiece(Resource):
    """
    Resource for editing puzzle pieces on a specified puzzle board.
    """
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument(
            'x_coordinate',
            type=int,
            help='The x-coordinate of the puzzle piece must be specified',
            required=True
        )
        self.parser.add_argument(
            'y_coordinate',
            type=int,
            help='The y-coordinate of the puzzle piece must be specified',
            required=True
        )

    def post(self, puzzle_id):
        """
        Endpoint for making a move to a position on the puzzle.
        """
        if not self.player_associated_with_puzzle(puzzle_id):
            return {'message': f'Puzzle requested does not exist or '
                               f'is not associated with {g.user.as_str()}.'}, 404

        # add parser for value
        self.parser.add_argument(
            'value',
            type=int,
            help='The value of the puzzle piece must be specified',
            required=True
        )
        args = self.parser.parse_args()
        try:
            puzzle = Puzzle.get_puzzle(puzzle_id)
            puzzle.update(
                x_coord=args['x_coordinate'],
                y_coord=args['y_coordinate'],
                value=args['value']
            )

            return {
                'message': f"Successfully saved the submission of {args['value']} at "
                           f"({args['x_coordinate']}, {args['y_coordinate']}) on "
                           f"puzzle_id {puzzle_id} by {g.user.as_str()}"
            }

        except PuzzleException as p_exception:
            return {'message': f'Attempt to save {args["value"]} at ({args["x_coordinate"]}, '
                               f'{args["y_coordinate"]}) on puzzle_id {puzzle_id}'
                               f' by user {g.user.as_str()} was unsuccessful',
                    'reason': p_exception.get_message()}, 400

        except Exception as exception:  # pylint: disable=broad-except
            print(f"Unexpected error: {exception}")
            return {'message': 'Unexpected error occurred while adding new value to puzzle'}, 500

    def delete(self, puzzle_id):
        """
        Deletes the current value currently stored in the puzzle
        """

        if not self.player_associated_with_puzzle(puzzle_id):
            return {'message': f'Puzzle requested does not exist or '
                               f'is not associated with {g.user.as_str()}.'}, 404

        args = self.parser.parse_args()
        try:
            puzzle = Puzzle.get_puzzle(puzzle_id)
            puzzle.update(
                x_coord=args['x_coordinate'],
                y_coord=args['y_coordinate'],
                value=None
            )

            # emit the puzzle update to all members of the room
            socketio.emit('puzzle_update', sudoku_to_dict(puzzle), room=puzzle_id)

            return {'message': f"Successfully deleted piece at position ({args['x_coordinate']}, "
                               f"{args['y_coordinate']}) on puzzle_id {puzzle_id}."}

        except PuzzleException as p_exception:
            return {'message': f'Attempt to delete piece at ({args["x_coordinate"]}, '
                               f'{args["y_coordinate"]}) on puzzle_id {puzzle_id}'
                               f' by user {g.user.as_str()} was unsuccessful',
                    'reason': p_exception.get_message()}, 400

        except Exception as exception:  # pylint: disable=broad-except
            print(f"Unexpected error: {exception}")
            return {'message': 'Unexpected error occurred while deleting value from puzzle'}, 500

    @staticmethod
    def player_associated_with_puzzle(puzzle_id):
        """
        Determine if the player making the request is associated with the puzzle
        they are submitting a change for.
        """
        # find all puzzles associated with the player making the request
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g.user.g_id)

        if not any(puzzle.puzzle_id == puzzle_id for puzzle in player_puzzles):
            return False
        return True
