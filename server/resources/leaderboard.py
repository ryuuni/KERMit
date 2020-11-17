from flask_restful import Resource, reqparse
from server.models.player import PuzzlePlayer


class Leaderboard(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('limit', type=int)

    def get(self):
        """
        Returns the top 10 users with the highest scores.
        """
        args = self.parser.parse_args()
        n_results = args['limit'] if args['limit'] is not None and args['limit'] < 1 else 10

        top_players = PuzzlePlayer.get_top_players(n_results)
        if not top_players:
            return {
                'message': 'No users have completed puzzles.',
                'puzzles': []
            }
        return {
            'players': [
                user_score_as_dict(
                    first_name=entry.first_name,
                    last_name=entry.last_name, 
                    score=entry.score
                )
                for entry in top_players
            ]
        }


def user_score_as_dict(first_name, last_name, score):
        """
        Helper function for converting a user + score into a dictionary
        """
        return {
            'first_name': first_name,
            'last_name': last_name,
            'score': score
        }


        

