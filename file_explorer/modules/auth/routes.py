from flask import Blueprint, render_template, request, jsonify, session
from core.server.state import get_password
import socket

auth_bp = Blueprint("auth", __name__)

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

def is_host_request(req):
    return req.remote_addr in ("127.0.0.1", "localhost", HOST_IP)

@auth_bp.route("/", methods=["GET", "POST"])
def index():
    if is_host_request(request):
        return render_template("indexhost.html")
    else:
        return render_template("index.html")
    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    password = data.get("password")

    stored_password = get_password()
    if not stored_password:
        return jsonify({"error": "Servidor ainda não configurado"}), 400

    if password == stored_password:
        session["authenticated"] = True
        return jsonify({"message": "Login bem-sucedido"}), 200

    return jsonify({"error": "Senha incorreta"}), 401
