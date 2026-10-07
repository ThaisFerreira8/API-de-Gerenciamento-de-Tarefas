"""Ponto de entrada e fábrica da aplicação Flask."""

import logging
import os

from flask import Flask, jsonify
from flask_migrate import Migrate

from app.database import db
from app import models  # noqa: F401: registra os modelos antes de criar as tabelas
from app.routes import api

migrate = Migrate()


def create_app(configuracao=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///tasks.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    if configuracao:
        app.config.update(configuracao)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api)

    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    @app.errorhandler(404)
    def rota_nao_encontrada(_erro):
        return jsonify({"erro": "Rota não encontrada."}), 404

    @app.errorhandler(500)
    def erro_interno(erro):
        app.logger.exception("Erro interno não tratado", exc_info=erro)
        return jsonify({"erro": "Erro interno do servidor."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
