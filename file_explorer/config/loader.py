import json
import os
from flask import current_app
import logging

_CONFIG_CACHE = {}

def load_json(filename: str, base_path: str = None) -> dict:
    """
    Carrega um arquivo JSON da pasta config/, com cache e logging.
    Retorna um dicionário, independentemente da estrutura do JSON.
    """
    global _CONFIG_CACHE
    if filename in _CONFIG_CACHE:
        return _CONFIG_CACHE[filename]

    if base_path is None:
        try:
            base_path = current_app.root_path
        except RuntimeError:
            base_path = os.getcwd()

    path = os.path.join(base_path, "config", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _CONFIG_CACHE[filename] = data
        return data
    except FileNotFoundError:
        logging.error(f"Arquivo de configuração não encontrado: {path}")
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao ler JSON do arquivo {path}: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado ao carregar JSON {path}: {e}")

    _CONFIG_CACHE[filename] = {}
    return {}
