from config.loader import load_json
import mimetypes
import os

INLINE_PREFIXES = ("image/", "video/", "audio/", "text/", "application/json", "application/pdf")

def is_inline(mime: str) -> bool:
    return any(mime.startswith(prefix) for prefix in INLINE_PREFIXES)

def get_mime_and_icon(filename: str):
    config = load_json("mime_map.json")
    icon_map = config.get("icon_map", [])
    mime_overrides = config.get("mime_overrides", {})

    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    mime = mime_overrides.get(ext, mimetypes.guess_type(filename)[0])
    if mime is None:
        mime = "application/octet-stream"

    as_attachment = not is_inline(mime)

    icon = next(
        (entry.get("icon", "file.png") for entry in icon_map if ext[1:] in entry.get("type", [])),
        "file.png"
    )

    return mime, icon, as_attachment
