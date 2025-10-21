from flask import Blueprint, request, jsonify, current_app
import os

api_bp = Blueprint("api", __name__)

@api_bp.route("/base-dir", methods=["POST"])
def set_base_dir():
    data = request.get_json()
    if not data or "path" not in data:
        return jsonify({"error": "Campo 'path' é obrigatório"}), 400

    path = data["path"]
    if not os.path.isdir(path):
        return jsonify({"error": "Diretório inválido"}), 400

    current_app.config["BASE_DIR"] = os.path.abspath(path)
    current_app.logger.info(f"Diretório base definido: {path}")

    return jsonify({"message": "Diretório base configurado com sucesso.", "base_dir": path}), 200
