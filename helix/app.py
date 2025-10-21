from flask import Flask
from core.logging.logger import setup_logger
from modules.files.routes import files_bp
from api.routes import api_bp

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    setup_logger(app)
    app.config["BASE_DIR"] = None

    app.register_blueprint(files_bp)
    app.register_blueprint(api_bp, url_prefix="/config")

    return app
