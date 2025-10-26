from flask import Blueprint, render_template, request, jsonify, session, redirect
from modules.auth.service import validate_password, check_login_attempts, record_failed_attempt, reset_attempts
from core.utils.network import is_host_request
from core.utils.session import check_session_timeout
from core.server.state import is_configured
from functools import wraps
import logging
import time

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        client_ip = request.remote_addr
        if not check_session_timeout():
            logger.warning(f"Tentativa de acesso não autenticado de {client_ip}")
            return jsonify({"error": "Não autenticado"}), 401
        logger.debug(f"Acesso autorizado para {client_ip} - {request.endpoint}")
        return f(*args, **kwargs)
    return decorated

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    password = data.get("password")
    client_ip = request.remote_addr

    if not check_login_attempts(client_ip):
        return jsonify({"error": "Muitas tentativas. Tente novamente mais tarde."}), 429

    if not validate_password(password):
        record_failed_attempt(client_ip)
        return jsonify({"error": "Senha incorreta"}), 401

    session["authenticated"] = True
    session["login_time"] = time.time()
    session["client_ip"] = client_ip
    reset_attempts(client_ip)
    logger.info(f"Login bem-sucedido para IP: {client_ip}")
    return jsonify({"message": "Login bem-sucedido"}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    client_ip = session.get("client_ip", "unknown")
    session.clear()
    logger.info(f"Logout realizado para IP: {client_ip}")
    return jsonify({"message": "Logout bem-sucedido"}), 200

@auth_bp.route("/")
def index():
    client_ip = request.remote_addr
    logger.info(f"Acesso à página inicial de {client_ip} - Host: {is_host_request(request)}")

    if is_configured() and session.get("authenticated") and not is_host_request(request):
        return redirect("/files")

    if is_host_request(request):
        return render_template("indexhost.html")
    return render_template("index.html")
