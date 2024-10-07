from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # configuration of database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///heroes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    # Importing routes
    from .routes import main

    app.register_blueprint(main)

    return app