from ..model.observer import Observer
from flask import jsonify, request
from project import app

observer = None


@app.route("/configure", methods=["POST"])
def configure():
    global observer
    observer = Observer(request.json["communication"], request.json["scenarios"])
    observer.start()

    return jsonify({"msg": "Observer Start"})
