from flask import Flask
from core.logging.logger import setup_logger
from modules.files.routes import files_bp
from api.routes import api_bp
from modules.auth.routes import auth_bp

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = "helix-secret-key"

    setup_logger(app)
    app.config["BASE_DIR"] = None

    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    app.logger.info("Aplicação Flask inicializada")

    return app
