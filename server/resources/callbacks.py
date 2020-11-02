from server.server import jwt
from server.models.revoked_tokens import RevokedTokens


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Called everytime client tries to access secure endpoints.
    Returns True or False depending on if the passed token in blacklisted
    """
    jti = decrypted_token['jti']
    return RevokedTokens.is_jti_blacklisted(jti)


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    """
    No authentication header provided.
    """
    return {'message': 'No JWT authentication header provided'}, 401


@jwt.invalid_token_loader
def invalid_token_callback(callback):
    """
    Token provided is invalid.
    """
    return {'message': 'Invalid token provided.'}, 401


@jwt.expired_token_loader
def expired_token_callback(callback):
    """
    Token has expired.
    """
    return {'message': 'Access token has expired'}, 401
