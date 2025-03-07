import tempfile
import os.path
import uuid

TMPDIR = tempfile.gettempdir()


def get_path_for_tempfile(ext: str):
    if not ext.startswith("."):
        ext = "." + ext

    return os.path.join(TMPDIR, str(uuid.uuid4()) + ext)
