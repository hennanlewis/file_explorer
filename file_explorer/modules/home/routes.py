from flask import Blueprint, render_template, redirect, session, request
from core.utils.network import is_host_request
from core.server.state import is_configured
import logging

home_bp = Blueprint("home", __name__)
logger = logging.getLogger(__name__)

@home_bp.route("/")
def index():
    client_ip = request.remote_addr
    logger.info(f"Acesso à página inicial de {client_ip} - Host: {is_host_request(request)}")

    if is_configured() and session.get("authenticated") and not is_host_request(request):
        return redirect("/files")

    if is_host_request(request):
        return render_template("indexhost.html")
    return render_template("index.html")
