from server.server import db
from server.models.user import User


class PuzzlePlayer(db.Model):

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
    def find_all_puzzles_for_player(cls, username):
        """
        Find all puzzles for a specific player based on the player's username.
        """
        user = User.find_by_username(username)
        return cls.query.filter_by(player_id=user.id).all()

    @classmethod
    def find_players_for_puzzle(cls, puzzle_id):
        """
        Returns a list of all users associated with a specific puzzle.
        """
        return User.query.join(PuzzlePlayer, PuzzlePlayer.player_id == User.id).filter_by(puzzle_id=1).all()

    def __str__(self):
        return f"PuzzlePlayer(player_id={self.player_id}, puzzle_id={self.puzzle_id})"

