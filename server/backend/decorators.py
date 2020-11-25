"""
Defines various function/route decorators used in handling requests.
"""
from flask import make_response, request
from backend import app, db
from backend.resources.authentication import verify_token


@app.before_first_request
def create_tables():
    """
    Creates all database tables relevant to this application,
    if the tables do not already exist, before the first request is handed
    """
    db.create_all()


@app.before_request
def handle_cors():
    """
    Approach to handle Cross Origin Resource Sharing; this approach
    allows requests for all origins. This approach was used after
    failure to get CORS(backend) simplistic approach to work with React. Instead,
    we ensure we enable access for OPTIONS pre-flight requests and returning
    approval. Inspiration for this approach from Niels B on StackOverflow at
    https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
    """
    def _build_cors_preflight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()


@app.before_request
def verify_oauth_token():
    """
    Method to run before all requests; determines if a user has a valid
    Google OAuth2 token and uses the token to discover who the user making the request is.
    The user is then loaded in from the database and stored in a special flask object called 'g'.
    While g is not appropriate for storing data across requests, it provides a global namespace
    for holding any data you want during a single backend context.
    """
    # allow the health check endpoint to be unauthenticated
    if request.endpoint is None:
        return None
    return verify_token(request)
