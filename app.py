"""
API REST Aztlan 26 - Flask.
Registro, comprobantes y dashboard de usuarios.
"""
import os

from flask import Flask, redirect, send_from_directory, url_for
from flask_cors import CORS
from flasgger import Swagger

import config
from models.registro import db
from routes.registro import bp as registro_bp
from routes.comprobante import bp as comprobante_bp
from routes.usuarios import bp as usuarios_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    if not config.DB_USE_MOCK:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = config.SQLALCHEMY_ENGINE_OPTIONS

    db.init_app(app)
    with app.app_context():
        db.create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda r: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }
    swagger_template = {
        "info": {
            "title": "API Aztlan 26",
            "description": "Registro de participantes, comprobantes y dashboard.",
            "version": "1.0.0",
        },
        "schemes": ["http", "https"],
    }
    Swagger(app, config=swagger_config, template=swagger_template)

    app.register_blueprint(registro_bp)
    app.register_blueprint(comprobante_bp)
    app.register_blueprint(usuarios_bp)

    # Redirigir raíz a Swagger UI
    @app.route("/")
    def index():
        return redirect(url_for("flasgger.apidocs"))

    # Servir archivos de comprobantes (para comprobanteUrl del dashboard)
    @app.route("/comprobantes/<path:filename>")
    def serve_comprobante(filename):
        folder = config.UPLOAD_FOLDER
        return send_from_directory(folder, filename)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", config.PORT))
    app.run(host="0.0.0.0", port=port, debug=True)
