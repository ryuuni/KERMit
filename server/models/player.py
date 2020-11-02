from server.server import db


class PuzzlePlayer(db.Model):

    __tablename__ = 'puzzle_players'

    player_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('sudoku_puzzle.id'), primary_key=True)

    def __init__(self, user_id, puzzle_id):
        self.user_id = user_id
        self.puzzle_id = puzzle_id

    def save(self):
        db.session.save(self)
        db.session.commit()

    @classmethod
    def find_all_puzzles_for_player(cls, player_id):
        return cls.query(PuzzlePlayer.puzzle_id).filter(player_id=player_id).all()

    @classmethod
    def find_all_players_for_puzzle(cls, puzzle_id):
        return cls.query(PuzzlePlayer.player_id).filter(puzzle_id=puzzle_id).all()

    def __str__(self):
        return f"PuzzlePlayer(player_id={self.player_id}, puzzle_id={self.puzzle_id})"

