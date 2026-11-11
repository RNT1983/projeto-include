import os

from flask import Flask, render_template
from app.extensions import db


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "chave-temporaria-para-desenvolvimento"

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///projeto_include.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
