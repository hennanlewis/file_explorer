import hashlib

SERVER_STATE = {
    "base_dir": None,
    "password": None
}

def set_base_dir(path: str):
    SERVER_STATE["base_dir"] = path

def get_base_dir():
    return SERVER_STATE.get("base_dir")

def set_password(password: str):
    SERVER_STATE["password"] = hashlib.sha256(password.encode()).hexdigest()

def get_password():
    return SERVER_STATE["password"]

def is_configured():
    return SERVER_STATE["base_dir"] is not None and SERVER_STATE["password"] is not None
