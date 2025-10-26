import time
from flask import session
from core.config import Config
import logging

logger = logging.getLogger(__name__)

def check_session_timeout():
    if session.get("authenticated") and session.get("login_time"):
        elapsed = time.time() - session["login_time"]
        if elapsed > Config.SESSION_TIMEOUT:
            session.clear()
            logger.info("Sessão expirada por timeout")
            return False
        session["login_time"] = time.time()
    return session.get("authenticated", False)
