from ..model.effector import Effector
from flask import jsonify, request
from project import app


effector = None
device, curent_status = None, None


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure", methods=["POST"])
def configure():
    global effector
    effector = Effector(request.json["adaptation_strategies"])
    return jsonify("Effector Configured")


@app.route("/adapt", methods=["GET"])
def adapt():
    global effector, device, current_status
    scenario = request.args.get("scenario")
    print(f"Scenario to adpat: {scenario}")
    device, current_status = effector.adapt(scenario)
    if current_status == "fail":
        return jsonify("Effector Failed"), 500

    return jsonify("Effector Successful"), 200


@app.route("/return_to_previous_state", methods=["GET"])
def return_to_previous_state():
    global effector, device, current_status

    print(f"Returning {device} to {current_status}...")
    response = effector.execute(device, current_status)

    if response == "success":
        return jsonify("Returned to previous state")

    return jsonify("Failed when returning to previous state"), 500
