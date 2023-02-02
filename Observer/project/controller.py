from flask import jsonify, request
from project import app
from flasgger import swag_from
from .observer import Observer

observer = None

@swag_from('swagger/health.yaml')
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"msg": "ok"})


@swag_from('swagger/configure.yaml')
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
