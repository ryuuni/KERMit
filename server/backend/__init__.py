"""
Makes backend a package; this prevents circular import Flask issues that are
encountered when putting the app in a file where it is imported into models/resources
and then needs to be re-imported.

Approach take from Corey Shafer tutorial named
"Python Flask Tutorial: Full-Featured Web App Part 5 - Package Structure"
found here: https://www.youtube.com/watch?v=44PvX0Yv368&feature=youtu.be
"""
import os
from flask_cors import CORS
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'backend.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

cors = CORS(app)
db = SQLAlchemy(app)
socketio = SocketIO(app, manage_session=True)
api = Api(app)

from backend import routes
