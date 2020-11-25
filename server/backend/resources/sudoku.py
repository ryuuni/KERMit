"""
Resources for creating, editing, and retrieving Sudoku Puzzle Board/Pieces.
"""
from flask import g
from flask_restful import Resource, reqparse
from backend.models.sudoku_puzzle import Puzzle
from backend.models.puzzle_exception import PuzzleException
from backend.models.player import PuzzlePlayer
from backend import db, socketio


class SudokuPuzzles(Resource):
    """
    Resource for retrieving and creating Sudoku puzzles for a user.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument(
            'difficulty',
            type=float,
            help='The difficulty of the puzzle must be specified',
            required=True
        )
        self.parser.add_argument(
            'size',
            type=int,
            help='The size of the puzzle must be specified',
            required=True
        )

    @staticmethod
    def get():
        """
        Returns all of the sudoku puzzles for the user making the request.
        """
        # based on the user, find all of their active puzzles
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g.user.g_id)

        if not player_puzzles:
            return {
                'message': f'No sudoku puzzles are associated with {g.user.as_str()}',
                'puzzles': []
            }

        # format all of the sudoku puzzles and return them
        return {
            'puzzles': [
                sudoku_to_dict(
                    puzzle=Puzzle.get_puzzle(puzzle.puzzle_id),
                    puzzle_players=PuzzlePlayer.find_players_for_puzzle(puzzle.puzzle_id)
                )
                for puzzle in player_puzzles
            ]
        }

    def post(self):
        """
        Creates a new sudoku puzzle, adding it to the database. The user making the request to
        create the new puzzle will be automatically added as the puzzle's first "player".
        """
        # parse the request body for arguments specifying game board to create the puzzle
        args = self.parser.parse_args()

        try:
            # do the database work
            new_puzzle = Puzzle(difficulty_level=args['difficulty'], size=args['size'])
            puzzle_id = new_puzzle.save(autocommit=False)

            # create new entry for player
            puzzle_player = PuzzlePlayer(player_id=g.user.id, puzzle_id=puzzle_id)
            puzzle_player.save(autocommit=False)

            # now commit all changes as a single transaction
            db.session.commit()
            return {
                'message': 'New Sudoku puzzle successfully created',
                'difficulty': args['difficulty'],
                'size': args['size'],
                'puzzle_id': puzzle_id
            }

        except PuzzleException as p_exception:
            return {'message': 'Failed to create new Sudoku Puzzle',
                    'reason': p_exception.get_message()}, 400  # bad request

        except Exception as exception:  # pylint: disable=broad-except
            print(f"Exception occurred while creating new puzzle: {exception}")
            return {'message': 'Failed to create new Sudoku Puzzle'}, 500


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
                value=args['value'],

            )

            # emit the puzzle update to all members of the room
            socketio.emit('puzzle_update', sudoku_to_dict(puzzle), room=puzzle_id)
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


class SudokuPuzzleSolution(Resource):
    """
    Resource for retrieving solutions for Sudoku puzzles,
    and comparing a current Sudoku puzzle state to that of the winning
    configuration.
    """
    @staticmethod
    def get(puzzle_id):
        """
        Returns the solved puzzle for a given puzzle id, as well as a list
        of the discrepancies in the current puzzle relative to the solved version.
        """
        # find all puzzles associated with the player making the request
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g.user.g_id)

        # if the requested puzzle doesn't exist for the user, then return error
        if not any(puzzle.puzzle_id == puzzle_id for puzzle in player_puzzles):
            return {'message': f"Puzzle requested does not exist or is not associated "
                               f"with user {g.user.as_str()}"}, 404  # not found

        # get the puzzle and return it back
        puzzle = Puzzle.get_puzzle(puzzle_id)
        return {
            'solved_puzzle': sudoku_to_dict(puzzle.get_solved_puzzle()),
            'discrepancy': puzzle.compare_with_solved_board()
        }


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
