import mimetypes
import os
import json
from flask import current_app

INLINE_PREFIXES = ("image/", "video/", "audio/", "text/", "application/json", "application/pdf")

CONFIG_CACHE = None

def load_config():
    global CONFIG_CACHE
    if CONFIG_CACHE is None:
        config_path = os.path.join(current_app.root_path, "config", "mime_map.json")
        with open(config_path, "r", encoding="utf-8") as f:
            CONFIG_CACHE = json.load(f)
    return CONFIG_CACHE

def get_mime_and_icon(filename):
    config = load_config()
    icon_map = config.get("icon_map", [])
    mime_overrides = config.get("mime_overrides", {})

    ext = "." + filename.split(".")[-1].lower()

    mime = mime_overrides.get(ext, mimetypes.guess_type(filename)[0])
    if mime is None:
        mime = "application/octet-stream"

    as_attachment = not mime.startswith(INLINE_PREFIXES)

    icon = "file.png"
    for entry in icon_map:
        if ext[1:] in entry.get("type", []):
            icon = entry.get("icon", "file.png")
            break

    return mime, icon, as_attachment
