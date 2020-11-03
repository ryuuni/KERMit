from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.user import User
from server.models.sudoku_puzzle import SudokuPuzzle
from server.models.puzzle_exception import PuzzleException
from server.models.player import PuzzlePlayer
from server.server import db

# create a new puzzle

# add new users to a puzzle

# add a new value to the puzzle

# return all puzzles for a user

# return a specific puzzle for a user

# return leaderboard scores


def get_request_username():
    return get_jwt_identity()


def sudoku_to_dict(puzzle, puzzle_players):
    """
    Converts information about a Sudoku board into a dictionary.
    """

    def puzzle_piece_as_dict(puzzle_piece):
        return {
            'x_coordinate': puzzle_piece.x_coordinate,
            'y_coordinate': puzzle_piece.y_coordinate,
            'static_piece': puzzle_piece.static_piece,
            'value': puzzle_piece.value
        }

    def user_as_dict(user):
        return {
            'username': user.username,
            'id': user.id
        }

    return {
        'puzzle_id': puzzle.id,
        'completed': puzzle.completed,
        'difficulty': puzzle.difficulty,
        'point_value': puzzle.point_value,
        'pieces': [puzzle_piece_as_dict(piece) for piece in puzzle.puzzle_pieces],
        'players': [user_as_dict(player) for player in puzzle_players]
    }


class SudokuPuzzles(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument(
            'difficulty',
            type=float,
            help='The difficulty of the puzzle must be specified',
            location='form',
            required=True
        )
        self.parser.add_argument(
            'size',
            type=int,
            help='The size of the puzzle must be specified',
            location='form',
            required=True
        )

    @jwt_required
    def get(self):
        """
        Returns all of the Sudoku Puzzles for the user making the request.
        """
        # based on the user, find all of their active puzzles
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(get_request_username())

        if not player_puzzles:
            return {'message': 'No sudoku puzzles are associated with this account'}

        # format all of the sudoku puzzles
        return {
            'puzzles': [
                sudoku_to_dict(
                    puzzle=SudokuPuzzle.get_puzzle(puzzle.puzzle_id),
                    puzzle_players=PuzzlePlayer.find_players_for_puzzle(puzzle.puzzle_id)
                )
                for puzzle in player_puzzles
            ]
        }

    @jwt_required
    def post(self):
        """
        Creates a new sudoku puzzle, adding it to the database. The user making the request to
        create the new puzzle will be automatically added as the puzzle's first "player".
        """
        # find the user making the request
        user = User.find_by_username(get_request_username())

        # parse the request body for arguments specifying game board to create the puzzle
        args = self.parser.parse_args()

        try:
            # do the database work
            new_puzzle = SudokuPuzzle(difficulty_level=args['difficulty'], size=args['size'])
            puzzle_id = new_puzzle.save(autocommit=False)

            # create new entry for player
            puzzle_player = PuzzlePlayer(player_id=user.id, puzzle_id=puzzle_id)
            puzzle_player.save(autocommit=False)

            # now commit all changes as a single transaction
            db.session.commit()
            return {
                'message': 'New Sudoku puzzle successfully created',
                'difficulty': args['difficulty'],
                'size': args['size'],
                'puzzle_id': puzzle_id
            }

        except PuzzleException as pe:
            return {
                'message': 'Failed to create new Sudoku Puzzle',
                'reason': pe.get_message()
            }, 400

        except Exception as e:
            print(f"Exception occurred while creating new puzzle: {e}")
            return {'message': 'Failed to create new Sudoku Puzzle'}, 500

#
# class SudokuPuzzle(Resource):
#
#     @jwt_required
#     def get(self, puzzle_id):
#         """
#         Finds all moves made on puzzle.
#         """
#         active_puzzles = PuzzlePlayer.find_active_puzzles(get_jwt_identity())
#
#         if not active_puzzles or puzzle_id not in active_puzzles:
#             return {'message': 'Puzzle does not exist'}, 404
#
#         return {
#             'sudoku': True
#         }
#
#
# class SudokuPuzzlePiece(Resource):
#
#     @jwt_required
#     def get(self, puzzle_id):
#         """
#         Finds all moves made on puzzle.
#         """
#         return {
#             'sudoku': True
#         }
#
#     @jwt_required
#     def post(self, puzzle_id):
#         """
#         Finds all moves made on puzzle.
#         """
#         return {
#             'sudoku': True
#         }


