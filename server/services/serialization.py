import pickle
from typing import Any
from flask import send_file


def serialize(model: Any, filename: str, extension=""):

    if extension == "":
        fpath = filename
    else:
        fpath = f"{filename}.{extension}"
    pickle.dump(model, open(fpath, "wb"))

    return send_file(fpath, mimetype="application/octet-stream")
