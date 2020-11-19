"""Player module

TODO: Flesh out documentation.

"""
from sqlalchemy import func
from server.server import db
from server.models.user import User
from server.models.sudoku_puzzle import Puzzle
from server.models.puzzle_exception import PuzzleException

MAX_PLAYERS_PER_PUZZLE = 4


class PuzzlePlayer(db.Model):
    """Puzzle player class

    TODO: Flesh out documentation

    """

    __tablename__ = 'puzzle_players'

    player_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('sudoku_puzzles.id'), primary_key=True)

    def __init__(self, player_id, puzzle_id):
        self.player_id = player_id
        self.puzzle_id = puzzle_id

    def save(self, autocommit=True):
        """
        Save a new puzzle-player paring to the database. Autocommit if specified.
        """
        db.session.add(self)

        if autocommit:
            db.session.commit()

    @classmethod
    def find_all_puzzles_for_player(cls, g_id):
        """
        Find all puzzles for a specific player based on the player's username.
        """
        user = User.find_by_g_id(g_id)
        return cls.query.filter_by(player_id=user.id).all()

    @classmethod
    def find_players_for_puzzle(cls, puzzle_id):
        """
        Returns a list of all users associated with a specific puzzle.
        """
        return User.query\
            .join(PuzzlePlayer, PuzzlePlayer.player_id == User.id)\
            .filter_by(puzzle_id=puzzle_id)\
            .all()

    @classmethod
    def get_top_players(cls, n_results):
        """
        Get the top players by cumulative score.
        """
        return (
            User.query
            .with_entities(User.first_name, User.last_name,
                           func.sum(Puzzle.point_value).label('score'))
            .join(PuzzlePlayer, PuzzlePlayer.player_id == User.id)
            .join(Puzzle, Puzzle.id == PuzzlePlayer.puzzle_id)
            .filter_by(completed=True)
            .group_by(User.id)
            .order_by(func.sum(Puzzle.point_value).desc())
            .limit(n_results)
        )

    @classmethod
    def add_player_to_puzzle(cls, puzzle_id, user):
        """
        Adds a new player to the puzzle based on their Google identifier.
        """
        # check if puzzle exists; in order to exist, it must be associated with at least 1 player
        existing_players = PuzzlePlayer.find_players_for_puzzle(puzzle_id)

        if not existing_players:
            raise PuzzleException("You cannot join a puzzle if the puzzle does not exist and "
                                  "have at least 1 player.")
        if len(existing_players) >= MAX_PLAYERS_PER_PUZZLE:
            raise PuzzleException(f"There are already {MAX_PLAYERS_PER_PUZZLE} "
                                  f"players affiliated with puzzle {puzzle_id}")

        puzzle_player = PuzzlePlayer(user.id, puzzle_id)
        puzzle_player.save(autocommit=True)

    def __str__(self):
        return f"PuzzlePlayer(player_id={self.player_id}, puzzle_id={self.puzzle_id})"
