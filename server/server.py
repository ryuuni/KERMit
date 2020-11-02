import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# ------  Set Configuration Settings ---------

app_settings = os.getenv(
    'APP_SETTINGS',
    'server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# -------- Setup Database and JWT ------------
db = SQLAlchemy(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()

# ----- Register endpoints and callbacks -------

# NOTE: Usually imports are made at top of file; however these must be imported after app is created in
# order to register properly
from server.resources.authentication import Registration, Login, LogoutAccess, LogoutRefresh, TokenRefresh, HealthCheck
from server.resources.sudoku import Sudoku
from server.resources.callbacks import invalid_token_callback, check_if_token_in_blacklist, \
    expired_token_callback, unauthorized_callback

api = Api(app)
api.add_resource(HealthCheck, '/hello')
api.add_resource(Registration, '/register')
api.add_resource(Login, '/login')
api.add_resource(LogoutAccess, '/logout/access')
api.add_resource(LogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Sudoku, '/puzzle')
