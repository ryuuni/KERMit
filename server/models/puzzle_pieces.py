"""
Module responsible for handling individual puzzle pieces (i.e., validation and
saving a specific value to the database for a given piece).
"""
from server.server import db  # db object from the file where db connection was initialized
from server.models.puzzle_exception import PuzzleException


class PuzzlePiece(db.Model):
    """
    Supports functionality related to individual puzzle pieces: finding pieces,
    validating piece changes, and storing updates.
    """
    __tablename__ = 'puzzle_pieces'
    __table_args__ = (
        db.UniqueConstraint('puzzle_id', 'x_coordinate', 'y_coordinate', name='unique_piece'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('sudoku_puzzles.id'), nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False)
    y_coordinate = db.Column(db.Integer, nullable=False)
    static_piece = db.Column(db.Boolean, nullable=False)
    value = db.Column(db.Integer, nullable=True)

    # pylint: disable=too-many-arguments
    def __init__(self, puzzle_id, x_coordinate, y_coordinate, value=None, static_piece=False):
        self.puzzle_id = puzzle_id
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value
        self.static_piece = static_piece

    @classmethod
    def find_all_pieces(cls, puzzle_id):
        """
        Find all pieces associated with a given puzzle id.
        """
        return cls.query.filter_by(puzzle_id=puzzle_id).all()

    @classmethod
    def get_piece(cls, puzzle_id, x_coordinate, y_coordinate):
        """
        Gets the requested piece, by puzzle id and coordinates on puzzle board.
        """
        piece = cls.query.filter_by(
            puzzle_id=puzzle_id,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate
        ).first()

        if not piece:  # this happens when the coordinates do not exist
            raise PuzzleException(f"No puzzle piece exists at ({x_coordinate}, {y_coordinate}). "
                                  f"This position is off of the puzzle board.")
        return piece

    def save(self, autocommit=False):
        """
        Saves a new "puzzle piece" to the database, autocommits if True.
        """
        db.session.add(self)
        # this allows for transactions when creating SudokuPuzzle instance and ALL pieces
        if autocommit:
            db.session.commit()

    def update(self, new_value, autocommit=False):
        """
        Updates the puzzle piece associated with the provided puzzle_id and coordinates
        with the new value specified.
        """

        if self.static_piece:  # you cannot change pieces that came with the game board
            raise PuzzleException("Changes can only be made to non-static puzzle pieces.")

        self.value = new_value
        if autocommit:
            db.session.commit()

    def __str__(self):
        return (
            f"PuzzlePiece(id={self.id}, puzzle_id={self.puzzle_id}, "
            f"x_coordinate={self.x_coordinate}, y_coordinate={self.y_coordinate}, "
            f"value={self.value}, static_piece={self.static_piece})"
        )
