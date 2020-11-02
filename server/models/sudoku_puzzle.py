import bcrypt
from server.models.puzzle_pieces import PuzzlePiece
from server.models.puzzle_exception import PuzzleException
from server.server import db
from sudoku import Sudoku

# range is 0 to 1
point_values = {
    (0.01, 0.24): 0,
    (0.25, 0.49): 25,
    (0.50, 0.74): 50,
    (0.75, 0.94): 75,
    (0.95, 0.99): 100
}


class SudokuPuzzle(db.Model):
    __tablename__ = 'sudoku_puzzles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    difficulty = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    point_value = db.Column(db.Integer, nullable=False)

    def __init__(self, difficulty_level=0.5, size=3, completed=False):
        self.difficulty = round(difficulty_level, 2)
        self.size = size
        self.point_value = self.assign_point_value()
        self.completed = completed

    def save_new_puzzle(self):
        """
        Saves a new Sudoku puzzle to the database. This automatically adds new records
        to SudokuPieces.
        """
        def save_new_puzzle_as_pieces():
            """
            Saves the individual puzzle pieces.
            """
            pieces = Sudoku(self.size).difficulty(self.difficulty).board  # produces 2D array of values
            for i in range(len(pieces)):
                for j in range(len(pieces[i])):
                    static_piece = True if pieces[i][j] else False
                    new_piece = PuzzlePiece(self.id, i, j, pieces[i][j], static_piece)
                    new_piece.save()

        # add the puzzle; allows the auto-increment id to be assigned to the puzzle, without commit
        db.session.add(self)
        db.session.flush()

        # save individual puzzle pieces
        save_new_puzzle_as_pieces()
        db.session.commit()

        # return the id of the newly generated puzzle
        return self.id

    @classmethod
    def get_existing_puzzle(cls, puzzle_id):
        """
        Returns the Puzzle matching the given id. If the puzzle doesn't exist, then None is returned.
        """
        return cls.query.filter_by(id=puzzle_id).first()  # returns None if no results matched

    def assign_point_value(self):
        """
        Based on the difficulty submitted, determines the point value associated with the puzzle.
        Harder puzzles receive higher point values.
        """
        if self.difficulty < 0.01 or self.difficulty > 0.99:
            raise PuzzleException(f"Difficulty levels must range between 0.01 and 0.99. Got {self.difficulty}.")

        intervals = list(point_values.keys())
        i = 0
        while i < len(intervals) and not (intervals[i][0] <= self.difficulty <= intervals[i][1]):
            i += 1
        return point_values[intervals[i]]

    def __str__(self):
        return f'SudokuPuzzle(id={self.id}, difficulty={self.difficulty}, completed={self.completed}), ' \
               f'point_value={self.point_value}, size={self.size})'
