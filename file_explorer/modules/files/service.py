from flask import send_file, abort
from core.services.file_manager import list_directory
from core.services.path_utils import resolve_path
from core.services.mime_resolver import get_mime_and_icon
import os

import logging

logger = logging.getLogger(__name__)

def get_directory_contents(subpath=""):
    target = resolve_path(subpath)
    return list_directory(target)

def get_file_response(filepath):
    try:
        full_path = resolve_path(filepath, must_be_file=True)
    except FileNotFoundError:
        abort(404)
    except Exception:
        abort(400)

    mime_type, _, as_attachment = get_mime_and_icon(full_path)

    filename = os.path.basename(full_path)

    return send_file(
        full_path,
        mimetype=mime_type,
        as_attachment=as_attachment,
        download_name=filename,
        conditional=True
    )
