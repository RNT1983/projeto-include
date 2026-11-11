from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "chave-temporaria-para-desenvolvimento"

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
