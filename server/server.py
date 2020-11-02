import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

# ---- Setup SQLAlchemy/Database connections ----

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


# ---- Setup the JWT Configurations ----

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)


# --------- Register endpoints and callbacks ----------

from server.resources.authentication import Registration, Login, LogoutAccess, LogoutRefresh, TokenRefresh
from server.resources.sudoku import Sudoku
from server.resources.callbacks import *

api.add_resource(Registration, '/register')
api.add_resource(Login, '/login')
api.add_resource(LogoutAccess, '/logout/access')
api.add_resource(LogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Sudoku, '/puzzle')
