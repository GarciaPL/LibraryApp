import os

from flask import Flask
from flasgger import Swagger  # type: ignore
from app.db.models import db

DATABASE_PATH = "db/data/database.db"


def create_app(test_config=None):
    app = Flask(__name__)

    print("== DEBUG: test_config =", test_config)

    if test_config:
        print("here")
        app.config.update(test_config)
    else:
        print("here 2")
        basedir = os.path.abspath(os.path.dirname(__file__))
        join_path = os.path.join(basedir, DATABASE_PATH)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + join_path

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    print("USING DB:", app.config["SQLALCHEMY_DATABASE_URI"])

    db.init_app(app)

    swagger = Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "LibraryApp",
                "description": "LibraryApp for managing books and wishlists",
                "version": "1.0",
            },
            "basePath": "/",
        },
    )

    from app.routes.home import bp as home

    app.register_blueprint(home)

    from app.routes.reports import bp as reports

    app.register_blueprint(reports)

    from app.routes.books import bp as books

    app.register_blueprint(books)

    from app.routes.rentals import bp as rentals

    app.register_blueprint(rentals)

    from app.routes.users import bp as users

    app.register_blueprint(users)

    from app.routes.wishlists import bp as wishlists

    app.register_blueprint(wishlists)

    return app
