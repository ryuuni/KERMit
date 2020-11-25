"""
Resource for getting a solution to a given puzzle.
"""
from flask import g
from flask_restful import Resource
from backend.models.player import PuzzlePlayer
from backend.models.sudoku_puzzle import Puzzle
from backend.resources.sudoku_puzzle import sudoku_to_dict


class SudokuPuzzleSolution(Resource):
    """
    Resource for retrieving solutions for Sudoku puzzles,
    and comparing a current Sudoku puzzle state to that of the winning
    configuration.
    """
    @staticmethod
    def get(puzzle_id):
        """
        Returns the solved puzzle for a given puzzle id, as well as a list
        of the discrepancies in the current puzzle relative to the solved version.
        """
        # find all puzzles associated with the player making the request
        player_puzzles = PuzzlePlayer.find_all_puzzles_for_player(g.user.g_id)

        # if the requested puzzle doesn't exist for the user, then return error
        if not any(puzzle.puzzle_id == puzzle_id for puzzle in player_puzzles):
            return {'message': f"Puzzle requested does not exist or is not associated "
                               f"with user {g.user.as_str()}"}, 404  # not found

        # get the puzzle and return it back
        puzzle = Puzzle.get_puzzle(puzzle_id)
        return {
            'solved_puzzle': sudoku_to_dict(puzzle.get_solved_puzzle()),
            'discrepancy': puzzle.compare_with_solved_board()
        }
