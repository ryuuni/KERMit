"""
Responsible for verification of the OAuth token submitted
before each request, as well as user registration.
"""
from flask import g
from flask_restful import Resource
from backend.models.user import User
from backend.google_auth import GoogleAuth


def verify_token(incoming_request):
    """
    The implementation of verification of token; separated from the method
    above for ease in testing.
    """
    if 'Authorization' not in incoming_request.headers:
        return {'message': 'Request denied access',
                'reason': 'Authorization header missing. Please provide an '
                           'OAuth2 Token with your request'}, 400

    auth_header = incoming_request.headers.get('Authorization')
    if 'Bearer ' not in auth_header:
        return {'message': 'Request denied access',
                'reason': "Malformed authorization header provided. Please make sure to "
                           "specify the header prefix correctly as 'Bearer ' and try again."}, 400

    # validate the token with Google
    access_token = auth_header.split("Bearer ")[1]

    is_valid, validation = is_valid_token(access_token)
    if not is_valid:
        return {'message': 'Request denied access',
                'reason': f'Google rejected oauth2 token: {validation["error_description"]}'}, 401

    g.access_token = access_token

    # unless this is a registration attempt, find the user associated with access token
    if incoming_request.endpoint != 'registration':
        user = User.find_by_g_id(validation['user_id'])
        if not user:
            return {'message': 'Request denied access',
                    'reason': 'User is not yet registered with this application; please '
                              'register before proceeding'}, 401

        # save this user for the rest of the request processing
        g.user = user
    return None  # hurray no issues!


def is_valid_token(token):
    """
    Takes a token, determines if it is valid and returns the validation resulting
    from the Google Auth API. Determines if the token is valid so that calling function
    does not need to do any additional checks to know the result, but can use the
    error description from the validation provided.
    """
    google_auth = GoogleAuth()
    validation = google_auth.validate_token(token)
    if 'error' in validation.keys():
        return False, validation
    return True, validation


class Registration(Resource):
    """
    Resource for registering a user with this puzzle API. Requires that an access_token
    is set.
    """
    google_auth = GoogleAuth()

    def post(self):
        """
        Endpoint for POST requests to register a new user with the sudoku puzzle system.
        """
        try:
            user_info = self.google_auth.get_user_information(g.access_token)
            if 'error' in user_info.keys():
                return {'message': 'User could not be registered',
                        'reason': 'User identity could not be found; valid OAuth2 access '
                                  'token not received.'}, 401

            if any(field not in user_info.keys() for field in ['id', 'email']):
                return {'message': 'User could not be registered',
                        'reason': "Google id (unique user identifier) and email must be "
                                  "retrievable attributes, but Google would not provide them."}, 401
        except Exception as exception:  # pylint: disable=broad-except
            print(f"Unexpected error occurred getting user info from Google: {exception}")
            return {'message': 'User could not be registered',
                    'reason': "Could not determine user information from Google using Oath2 token"
                              "for unknown reason"}, 500

        try:
            # does user with user id already exist?
            if User.find_by_g_id(user_info['id']):
                return {'message': f'User with Google ID {user_info["id"]} is already registered.'}

            new_user = User(
                g_id=user_info['id'],
                first_name=user_info['given_name'] if 'given_name' in user_info.keys() else None,
                last_name=user_info['family_name'] if 'family_name' in user_info.keys() else None,
                email=user_info['email']
            )
            new_user.save()
            return {'message': 'User {} {} was successfully registered'.format(
                                new_user.first_name, new_user.last_name)}

        except Exception as exception:  # pylint: disable=broad-except
            print(f"Unexpected error occurred registering new user in db: {exception}")
            return {'message': 'User could not be registered.',
                    'reason': f'An unknown error occurred {exception}'}, 500
