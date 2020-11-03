import bcrypt
from server.models.puzzle_pieces import PuzzlePiece
from server.models.puzzle_exception import PuzzleException
from server.server import db
from sudoku import Sudoku


class Puzzle(db.Model):
    __tablename__ = 'sudoku_puzzles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    difficulty = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    point_value = db.Column(db.Integer, nullable=False)

    # full available range is 0 to 1
    POINT_VALUES_DIFFICULTY = {
        (0.01, 0.24): 10,
        (0.25, 0.49): 25,
        (0.50, 0.74): 50,
        (0.75, 0.94): 75,
        (0.95, 0.99): 100
    }

    POINT_VALUES_SIZE = {
        2: 20,
        3: 40,
        4: 60,
        5: 80
    }

    SIZE_RANGE = (2, 5)
    DIFFICULTY_RANGE = (0.01, 0.99)

    def __init__(self, difficulty_level=0.5, size=3, completed=False):
        self.difficulty = None
        self.size = None
        self.point_value = None
        self.puzzle_pieces = []
        self.completed = completed

        self.set_difficulty(difficulty_level)
        self.set_size(size)
        self.set_point_value()
        self.set_pieces()

    @classmethod
    def get_puzzle(cls, puzzle_id):
        """
        Returns the Puzzle matching the given id. If the puzzle doesn't exist, then None is returned.
        """
        puzzle = cls.query.filter_by(id=puzzle_id).first()  # returns None if no results matched
        if not puzzle:
            return None

        # load in the puzzle pieces for the puzzle
        puzzle.puzzle_pieces = PuzzlePiece.find_all_pieces(puzzle_id=puzzle_id)
        return puzzle

    def save(self, autocommit=True):
        """
        Saves a new Sudoku puzzle to the database. This automatically adds new records
        to SudokuPieces.
        """
        # add the puzzle and flush; this allows the auto-increment id to be assigned to current puzzle, without commit
        db.session.add(self)
        db.session.flush()

        # save individual puzzle pieces
        for puzzle_piece in self.puzzle_pieces:
            puzzle_piece.puzzle_id = self.id
            puzzle_piece.save(autocommit=False)

        if autocommit:  # commit the changes, if requested
            db.session.commit()

        # return the id of the newly generated puzzle
        return self.id

    def set_difficulty(self, difficulty):
        """
        Checks to make sure that the difficulty level of the requested Sudoku board is supported.
        """
        if not isinstance(difficulty, float):
            raise PuzzleException(f"Sudoku puzzle difficulty specified must be a float value. "
                                  f"Got {difficulty} ({type(difficulty)}).")

        min_difficulty = self.DIFFICULTY_RANGE[0]
        max_difficulty = self.DIFFICULTY_RANGE[1]

        if difficulty < min_difficulty or difficulty > max_difficulty:
            raise PuzzleException(f"Difficulty levels must range between "
                                  f"{min_difficulty} and {max_difficulty}. Got {difficulty}.")
        self.difficulty = difficulty

    def set_size(self, size):
        """
        Checks to make sure that the size of the requested Sudoku board is supported.
        """
        if not isinstance(size, int):
            raise PuzzleException(f"Sudoku puzzle sizes specified must be valid integers. "
                                  f"Got {size} ({type(size)}).")

        if size not in range(self.SIZE_RANGE[0], self.SIZE_RANGE[1] + 1):
            raise PuzzleException(f"Valid sizes range from {self.SIZE_RANGE[0]} to {self.SIZE_RANGE[1]}. "
                                  f"Got {size}.")
        self.size = size

    def set_pieces(self):
        """
        Set the puzzle pieces for the Sudoku board.
        """
        pieces = Sudoku(self.size).difficulty(self.difficulty).board  # produces 2D array of values
        for i in range(len(pieces)):
            for j in range(len(pieces[i])):
                static_piece = True if pieces[i][j] else False
                new_piece = PuzzlePiece(self.id, i, j, pieces[i][j], static_piece)
                self.puzzle_pieces.append(new_piece)

    def set_point_value(self):
        """
        Based on the difficulty submitted, determines the point value associated with the puzzle.
        Harder puzzles receive higher point values.
        """
        # find points for difficulty
        difficulty_intervals = list(self.POINT_VALUES_DIFFICULTY.keys())
        i = 0
        while i < len(difficulty_intervals) and not \
                (difficulty_intervals[i][0] <= self.difficulty <= difficulty_intervals[i][1]):
            i += 1
        difficulty_points = self.POINT_VALUES_DIFFICULTY[difficulty_intervals[i]]

        # find points for size
        size_points = self.POINT_VALUES_SIZE[self.size]

        # set point value as sum of points for difficulty and size
        self.point_value = difficulty_points + size_points

    def update(self, x_coord, y_coord, value):
        """
        Update a puzzle with the specified value at the x, y coordinate on the puzzle board.
        """
        if self.completed:  # do not accept any changes to completed puzzles
            raise PuzzleException('Updates cannot be made to previously completed puzzles.')

        # update the piece in order to test if the puzzle is now complete
        for piece in self.puzzle_piecies:
            if piece.x_coordinate == x_coord and piece.y_coordinate == y_coord:
                piece.update(value, autocommit=False)

        if self.check_for_completion():
            self.set_puzzle_complete()

        # save all changes (change to the puzzle piece and the status of the
        db.session.commit()

    def check_for_completion(self):
        """
        Check if a puzzle is complete (i.e., has a winning configuration)
        """
        # if there are any None values, then puzzle has to be incomplete
        if any(piece.value is None for piece in self.puzzle_pieces):
            return False

        # rebuild original sudoku puzzle form static pieces
        original_board = self.get_piecies_as_arr(self.size, self.puzzle_pieces, static_only=True)
        current_board = self.get_piecies_as_arr(self.size, self.puzzle_pieces)

        # check against python sudoku
        solved_board = Sudoku(self.size, self.size, board=original_board).solve().board
        return solved_board == current_board

    def set_puzzle_complete(self, autocommit=False):
        """
        Sets a puzzle as 'completed.'
        """
        self.completed = True
        if autocommit:
            db.session.commit()

    def recreate_original_puzzle_as_array(self):
        """
        Recreates the original puzzle.
        """
        return self.get_piecies_as_arr(self.size, self.puzzle_pieces, static_only=True)

    @staticmethod
    def get_pieces_as_arr(size, puzzle_pieces, static_only=False):
        """
        Converts puzzle pieces into a 2D array representing the sudoku puzzle board.
        """
        dimensions = size * size
        arr = [[None for x in range(dimensions)] for y in range(dimensions)]

        for piece in puzzle_pieces:
            if piece.static_piece or not static_only:
                arr[piece.x_coordinate][piece.y_coordinate] = piece.value
        return arr

    def __str__(self):
        return f'SudokuPuzzle(id={self.id}, difficulty={self.difficulty}, completed={self.completed}), ' \
               f'point_value={self.point_value}, size={self.size})'
