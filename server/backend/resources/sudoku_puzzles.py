"""
Resource for getting all puzzles associated with a user, or creating a new puzzle.
"""
from flask import g
from flask_restful import Resource, reqparse
from backend import db
from backend.models.player import PuzzlePlayer, MAX_PLAYERS_PER_PUZZLE
from backend.models.puzzle_exception import PuzzleException
from backend.models.sudoku_puzzle import Puzzle
from backend.models.user import User
from backend.resources.sudoku_puzzle import sudoku_to_dict


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
        self.parser.add_argument(
            'additional_players',
            help='The list of users to add to the puzzle; may be an empty list',
            action='append'
        )

    @staticmethod
    def get():
        """
        Returns all of the sudoku puzzles for the user making the request;
        by default, returns only the "visible" and not hidden puzzles.
        """
        # based on the user, find all of their active puzzles
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g.user.g_id, hidden=False)

        if not player_puzzles:
            return {
                'message': f'No unhidden sudoku puzzles are associated with {g.user.as_str()}',
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
        additional_emails = args.get('additional_players')
        if additional_emails and len(additional_emails) + 1 > MAX_PLAYERS_PER_PUZZLE:
            return {'message': 'Failed to create new Sudoku Puzzle',
                    'reason': f'Too many additional players have been specified; the total '
                              f'number of players allowed per puzzle '
                              f'is {MAX_PLAYERS_PER_PUZZLE}'}, 400

        try:
            # do the database work
            new_puzzle = Puzzle(difficulty_level=args['difficulty'], size=args['size'])
            puzzle_id = new_puzzle.save(autocommit=False)

            # create new entry for player
            puzzle_player = PuzzlePlayer(player_id=g.user.id, puzzle_id=puzzle_id)
            puzzle_player.save(autocommit=False)

            # add any subsequent users that the player requested to add to their puzzle
            players_registered, players_unregistered = User.find_users_by_email(
                emails=set(additional_emails) if additional_emails else []
            )
            for player in players_registered:
                if player.id != g.user.id:
                    PuzzlePlayer.add_player_to_puzzle(puzzle_id, player, autocommit=False)

            # now commit all changes as a single transaction
            db.session.commit()
            return {
                'message': 'New Sudoku puzzle successfully created',
                'difficulty': args['difficulty'],
                'size': args['size'],
                'puzzle_id': puzzle_id,
                'unregistered_emails': players_unregistered
            }

        except PuzzleException as p_exception:
            return {'message': 'Failed to create new Sudoku Puzzle',
                    'reason': p_exception.get_message()}, 400  # bad request

        except Exception as exception:  # pylint: disable=broad-except
            print(f"Exception occurred while creating new puzzle: {exception}")
            return {'message': 'Failed to create new Sudoku Puzzle'}, 500
