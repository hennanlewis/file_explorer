import os
from core.services.mime_resolver import get_mime_and_icon

def list_directory(path):
    entries = []
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return entries
    except FileNotFoundError:
        return entries

    for name in items:
        full_path = os.path.join(path, name)
        try:
            is_dir = os.path.isdir(full_path)
            mime, icon, mi = get_mime_and_icon(name)
            entries.append({
                "name": name,
                "path": os.path.relpath(full_path, path),
                "is_dir": is_dir,
                "icon": "folder.png" if is_dir else icon,
                "mime": mime
            })

        except PermissionError as e:
            logger.warning(f"Sem permissão para acessar: {full_path}")
            continue

    entries.sort(key=lambda e: (not e["is_dir"], e["name"].lower()))

    return entries
