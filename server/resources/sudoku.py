from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required


class Sudoku(Resource):

    @jwt_required
    def get(self):
        """
        Access to endpoint requires valid JWT access token (refresh token will not work).
        """
        return {
            'sudoku': True
        }