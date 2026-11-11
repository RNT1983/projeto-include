
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "chave-temporaria-para-desenvolvimento"

    @app.route("/")
    def index():
        return {
            "projeto": "Projeto Include",
            "mensagem": "Aplicação iniciada com sucesso!"
        }

    return app
