import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(32)
    BASE_DIR = None
    SESSION_TIMEOUT = 3600
    MAX_LOGIN_ATTEMPTS = 5
