import os
from flask import current_app, abort

def get_base_dir():
    base_dir = current_app.config.get("BASE_DIR")
    if not base_dir:
        abort(400, "Diretório base não configurado.")
    return base_dir

def resolve_path(subpath, must_exist=True, must_be_file=False):
    base_dir = get_base_dir()
    full_path = os.path.join(base_dir, subpath)

    if must_exist and not os.path.exists(full_path):
        abort(404, f"Caminho não encontrado: {subpath}")

    if must_be_file and not os.path.isfile(full_path):
        abort(404, f"Arquivo não encontrado: {subpath}")

    return full_path
