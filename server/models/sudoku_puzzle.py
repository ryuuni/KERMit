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

        if autocommit:  # commit all the changes, if requested
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
                new_piece = PuzzlePiece(self.id, j, i, pieces[i][j], static_piece)
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

        # make sure that the coordinate is in the puzzle
        coord_range = self.size * self.size
        if (x_coord >= coord_range or x_coord < 0) or (y_coord >= coord_range or y_coord < 0):
            raise PuzzleException(f'Coordinates provided ({x_coord}, {y_coord}) are outside the range of '
                                  f'the puzzle. Available coordinates are (0, 0) to ({coord_range}, {coord_range}).')

        # make sure that the value is valid for the puzzle
        value_range = coord_range
        if value > value_range or value <= 0:
            raise PuzzleException(f'Invalid value provided ({value}). the range of the puzzle. '
                                  f'Available values are 1 to {value_range}.')

        # update the piece in order to test if the puzzle is now complete
        for piece in self.puzzle_pieces:
            if piece.x_coordinate == x_coord and piece.y_coordinate == y_coord:
                piece.update(value, autocommit=False)
                break

        if self.is_complete_puzzle():
            self.set_puzzle_complete()

        # save all changes (change to the puzzle piece and the status of the
        db.session.commit()

    def is_complete_puzzle(self):
        """
        Check if a puzzle is complete (i.e., has a winning configuration)
        """
        # if there are any None values, then puzzle has to be incomplete
        if any(piece.value is None for piece in self.puzzle_pieces):
            return False

        # rebuild original sudoku puzzle form static pieces
        discrepancies = self.compare_with_solved_board()
        return True if not discrepancies else False

    def set_puzzle_complete(self, autocommit=False):
        """
        Sets a puzzle as 'completed.'
        """
        self.completed = True
        if autocommit:
            db.session.commit()

    def compare_with_solved_board(self):
        """
        Compares the current Sudoku puzzle with the solved board and gets a list
        of indices that do not match.
        """
        solved_board = self.get_solved_puzzle()
        current_board_arr = self.get_pieces_as_arr()
        solved_board_arr = solved_board.get_pieces_as_arr()

        discrepancies = []
        for y_coord in range(len(solved_board_arr)):
            for x_coord in range(len(solved_board_arr[y_coord])):
                if current_board_arr[y_coord][x_coord] != solved_board_arr[y_coord][x_coord]:
                    discrepancies.append({'x_coordinate': x_coord, 'y_coordinate': y_coord})

        return discrepancies

    def recreate_original_puzzle_as_array(self):
        """
        Recreates the original empty puzzle based on the static only pieces.
        """
        return self.get_pieces_as_arr(static_only=True)

    def get_solved_puzzle(self):
        original_arr = self.recreate_original_puzzle_as_array()
        solved_arr = Sudoku(self.size, self.size, board=original_arr).solve().board

        # create the winning puzzle board
        pieces = []
        for idx_row in range(len(solved_arr)):
            for idx_column in range(len(solved_arr[idx_row])):
                static = True if original_arr[idx_row][idx_column] else False
                pieces.append(
                    PuzzlePiece(
                        puzzle_id=self.id,
                        x_coordinate=idx_column,
                        y_coordinate=idx_row,
                        value=solved_arr[idx_row][idx_column],
                        static_piece=static
                    )
                )

        solved_board = Puzzle(self.difficulty, self.size, True)
        solved_board.puzzle_pieces = pieces
        return solved_board

    def get_pieces_as_arr(self, static_only=False):
        """
        Converts puzzle pieces into a 2D array representing the sudoku puzzle board.
        """
        dimensions = self.size * self.size
        arr = [[None for _ in range(dimensions)] for __ in range(dimensions)]

        for piece in self.puzzle_pieces:
            if piece.static_piece or not static_only:
                arr[piece.y_coordinate][piece.x_coordinate] = piece.value
        return arr

    def __str__(self):
        return f'SudokuPuzzle(id={self.id}, difficulty={self.difficulty}, completed={self.completed}), ' \
               f'point_value={self.point_value}, size={self.size})'
