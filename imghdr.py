# --- Shim for imghdr (removed in Python 3.13) ---
# This is a minimal reimplementation that works for Telegram Bot

def what(file, h=None):
    """Return file type if recognizable, else None"""
    if h is None:
        if hasattr(file, "read"):
            pos = file.tell()
            h = file.read(32)
            file.seek(pos)
        else:
            with open(file, "rb") as f:
                h = f.read(32)

    # JPEG
    if h[0:3] == b"\xff\xd8\xff":
        return "jpeg"
    # PNG
    if h[0:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    # GIF
    if h[0:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    # BMP
    if h[0:2] == b"BM":
        return "bmp"
    # WEBP
    if h[8:12] == b"WEBP":
        return "webp"

    return None
