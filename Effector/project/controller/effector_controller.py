from project.entity.effector_entity import Effector
from flask import jsonify, request
from project import app


effector = None


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/adapt", methods=["GET"])
def adapt():
    global effector
    scenario = request.args.get("scenario")
    effector.adapt(scenario)

    return jsonify({"msg": "Adaptation ocurred"})


@app.route("/behave_normal", methods=["GET"])
def behave_normal():
    global effector
    scenario = request.args.get("scenario")
    effector.behave_normal(scenario)

    return jsonify({"msg": "Returned to previous behavior"})


@app.route("/configure", methods=["POST"])
def configure():
    global effector
    effector = Effector(
        request.json["adaptation_actions"],
        request.json["return_to_normal_actions"]
    )
    print("Start OK")
    return jsonify({"msg": "ok"})

