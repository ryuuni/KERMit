from server.server import db  # db object from the file where db connection was initialized
from server.models.puzzle_exception import PuzzleException


class PuzzlePiece(db.Model):
    __tablename__ = 'puzzle_pieces'
    __table_args__ = (
        db.UniqueConstraint('game_id', 'x_coordinate', 'y_coordinate', name='unique_piece'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('sudoku_puzzles.id'))
    x_coordinate = db.Column(db.Integer, nullable=False)
    y_coordinate = db.Column(db.Integer, nullable=False)
    static_piece = db.Column(db.Boolean, nullable=False)
    value = db.Column(db.Integer)

    def __init__(self, puzzle_id, x_coordinate, y_coordinate, value=None, static_piece=False):
        self.puzzle_id = puzzle_id
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value
        self.static_piece = static_piece

    def save(self, commit=False):
        """
        Saves a new "puzzle piece" to the database. Optionally, you can auto-commit this puzzle piece.
        """
        db.session.add(self)
        if commit:  # this allows for transactions when creating SudokuPuzzle instance and ALL pieces
            db.session.commit()

    @classmethod
    def find_all_pieces(cls, puzzle_id):
        """
        Find all pieces associated with a given puzzle id.
        """
        return cls.query.filter_by(puzzle_id=puzzle_id).all()

    @classmethod
    def update_piece(cls, puzzle_id, x_coordinate, y_coordinate, new_value):
        """
        Updates the puzzle piece associated with the provided puzzle_id and coordinates
        with the new value specified.
        """
        piece = cls.query.filter_by(
            puzzle_id=puzzle_id,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate
        ).one()

        if not piece:
            raise PuzzleException(f"No puzzle piece was found at ({x_coordinate}, {y_coordinate}).")

        if piece.static_piece:
            raise PuzzleException(f"Changes can only be made to non-static puzzle pieces. The item at "
                                  f"({x_coordinate}, {y_coordinate}) is a set piece in the puzzle.")
        piece.value = new_value
        db.session.commit()

    def __str__(self):
        return f'PuzzlePiece(id={self.id}, puzzle_id={self.puzzle_id}), x_coordinate={self.x_coordinate}, ' \
               f'y_coordinate={self.y_coordinate}, value={self.value}, static_piece={self.static_piece})'

