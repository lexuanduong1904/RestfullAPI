from flask import Flask
from .controller import users
from .controllerA import admins
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "vftyuikmncxdfghjkloiuygfcvbhjkweqeqeq"
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.register_blueprint(users)
    app.register_blueprint(admins)
    return app