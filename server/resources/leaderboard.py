from flask_restful import Resource, reqparse
from server.models.player import PuzzlePlayer
from server.server import db
from flask import g


class Leaderboard(Resource):

    def get(self):
        """
        Returns the top 10 users with the highest scores.
        """
        top_players = PuzzlePlayer.get_top_players()
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
        """Helper function for converting a user into a dictionary"""
        return {
            'first_name': first_name,
            'last_name': last_name,
            'score': score
        }


        

