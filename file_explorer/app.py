from flask import Flask
from core.config import Config
from core.logging.logger import setup_logger
from modules.auth.routes import auth_bp
from modules.files.routes import files_bp
from modules.home.routes import home_bp
from api.routes import api_bp

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    setup_logger(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    app.logger.info("Aplicação Flask inicializada")
    return app
