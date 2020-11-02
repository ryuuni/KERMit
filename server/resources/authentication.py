from flask_restful import Resource, reqparse
from server.models.user import User
from server.models.revoked_tokens import RevokedTokens
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


# define parser to get username/password from request
parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class HealthCheck(Resource):
    def get(self):
        return {'status': 'OK'}


class Registration(Resource):
    def post(self):
        data = parser.parse_args()

        # see if user already exists
        if User.find_by_username(data['username']):
            return {'message': 'Username {} is already taken'.format(data['username'])}, 403

        new_user = User(username=data['username'], password=data['password'])
        try:
            # save the new user to the database
            new_user.save()

            # create access/refresh tokens for the user
            return {
                'message': 'User {} was successfully created'.format(data['username']),
                'access_token': create_access_token(identity=data['username']),
                'refresh_token': create_refresh_token(identity=data['username'])
            }

        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            return {'message': f'An error occurred attempting to register new user {e}'}, 500


class Login(Resource):
    def post(self):
        data = parser.parse_args()

        # does the username exist?
        user = User.find_by_username(data['username'])
        if not user:
            return {'message': 'User {} does not exist'.format(data['username'])}, 404

        # is the password correct?
        correct_password = User.check_password(
            pt_password=data['password'],
            hashed_password=user.hashed_password
        )

        if correct_password:

            # create access/refresh tokens for the user
            return {
                'message': 'Logged in as {}'.format(user.username),
                'access_token': create_access_token(identity=data['username']),
                'refresh_token': create_refresh_token(identity=data['username'])
            }

        return {'message': 'Incorrect password'}, 401


class LogoutAccess(Resource):
    """
    When a user logs out, we need to add old tokens to the 'blacklist'
    """
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokens(jti=jti, token_type='access')
            revoked_token.add_to_blacklist()
            return {'message': 'Access token has been revoked'}

        except Exception as e:
            print(f"Unexpected error occurred on revoking access token: {e}")
            return {'message': 'Error occurred while revoking access token'}, 500


class LogoutRefresh(Resource):
    """
    When a user logs out, we need to add old tokens to the 'blacklist'
    """
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokens(jti=jti, token_type='refresh')
            revoked_token.add_to_blacklist()
            return {'message': 'Refresh token has been revoked'}

        except Exception as e:
            print(f"Unexpected error occurred on revoking refresh token: {e}")
            return {'message': 'Error occurred while revoking refresh token'}, 500


class TokenRefresh(Resource):
    """
    By default, access tokens have 15 minute lifetime; refresh tokens have
    a 30 day lifetime. To prevent users from having to login often you can reissue
    new access tokens using the refresh token.
    """

    @jwt_refresh_token_required
    def post(self):
        """
        Only accessible if you have a refresh token
        """
        # identify the user by extracting identity from refresh token
        user = get_jwt_identity()

        # generate a new access token and return it to users
        access_token = create_access_token(identity=user)
        return {
            'access_token': access_token
        }
