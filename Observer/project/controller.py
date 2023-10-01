from flask import jsonify, request
from project import app

from .observer import Observer, adaptation_status, cautious_status

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


@app.route("/get_adaptation_status", methods=["GET"])
def get_adaptation_status():
    if request.args.get("type") == "adaptation":
        if observer.adaptation_status or adaptation_status:
            return jsonify(observer.adaptation_status), 200
        return jsonify(observer.adaptation_status), 400

    if request.args.get("type") == "cautious":
        if observer.cautious_status or cautious_status:
            return jsonify(observer.cautious_status), 200
        return jsonify(observer.cautious_status), 400
