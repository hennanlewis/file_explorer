from flask import Blueprint, render_template
from modules.files.service import get_directory_contents, get_file_response

files_bp = Blueprint("files", __name__)

@files_bp.route("/files", defaults={"subpath": ""})
@files_bp.route("/files/<path:subpath>")
def list_files(subpath):
    items = get_directory_contents(subpath)
    breadcrumbs = subpath.split("/") if subpath else []
    return render_template("files.html", items=items, breadcrumbs=breadcrumbs, subpath=subpath)

@files_bp.route("/file/<path:filepath>")
def get_file(filepath):
    return get_file_response(filepath)
