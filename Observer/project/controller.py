from flask import jsonify, request
from project import app

from .observer import Observer

observer = None


@app.route("/configure", methods=["POST"])
def configure():
    global observer
    observer = Observer(
        request.json["communication"],
        request.json["scenarios"],
        request.json["project"],
    )
    observer.start()

    return jsonify({"msg": "Observer Start"})
