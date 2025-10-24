from flask import Blueprint, request, jsonify, current_app
import os, socket
from core.server.state import set_base_dir, set_password, get_base_dir, get_password

api_bp = Blueprint("api", __name__)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

HOST_IP = get_host_ip()

def is_host(request):
    return request.remote_addr in ("127.0.0.1", "localhost", HOST_IP)

@api_bp.route("/config", methods=["GET", "POST"])
def config():
    if not is_host(request):
        return jsonify({"error": "Acesso restrito ao host"}), 403

    if request.method == "POST":
        data = request.get_json() or {}
        base_dir = data.get("base_dir")
        password = data.get("password")

        if base_dir and os.path.isdir(base_dir):
            set_base_dir(os.path.abspath(base_dir))
            current_app.config["BASE_DIR"] = base_dir
        else:
            return jsonify({"error": "Diretório inválido"}), 400

        if password:
            set_password(password)
        else:
            return jsonify({"error": "Senha é obrigatória"}), 400

        return jsonify({"message": "Configurações salvas com sucesso"}), 200

    return jsonify({
        "base_dir": get_base_dir(),
        "password": "******" if get_password() else None
    })
