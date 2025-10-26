import hashlib
from core.server.state import get_password
from core.config import Config
import time
import logging

logger = logging.getLogger(__name__)

LOGIN_ATTEMPTS = {}

def validate_password(password: str) -> bool:
    stored = get_password()
    if not stored:
        return False
    return hashlib.sha256(password.encode()).hexdigest() == stored

def check_login_attempts(client_ip: str) -> bool:
    attempts = LOGIN_ATTEMPTS.get(client_ip, 0)
    if attempts >= Config.MAX_LOGIN_ATTEMPTS:
        logger.warning(f"Tentativas de login excedidas para IP: {client_ip}")
        return False
    return True

def record_failed_attempt(client_ip: str):
    LOGIN_ATTEMPTS[client_ip] = LOGIN_ATTEMPTS.get(client_ip, 0) + 1
    logger.warning(f"Tentativa de login falha para IP: {client_ip} - Tentativa {LOGIN_ATTEMPTS[client_ip]}")

def reset_attempts(client_ip: str):
    LOGIN_ATTEMPTS[client_ip] = 0
