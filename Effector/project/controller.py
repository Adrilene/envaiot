import os

from datetime import datetime
from dotenv import load_dotenv
from flask import jsonify, request
from project import app

from .effector import Effector
from .utils import write_log

effector = None
device, curent_status = None, None
load_dotenv()
adaptation_status = False


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure", methods=["POST"])
def configure():
    global effector
    effector = Effector(request.json["strategies"])
    return jsonify("Effector Configured")


@app.route("/adapt", methods=["GET"])
def adapt():
    global effector, device, current_status, adaptation_status, result

    scenario = request.args.get("scenario")
    adapt_type = request.args.get("adapt_type")

    write_log(f"Adapting {adapt_type} for {scenario}.")

    print(f"ADAPT: {scenario} - {adapt_type}")
    results = effector.adapt(scenario, adapt_type)
    count_fail = 0
    for result in results:
        if result[1] == "fail":
            count_fail += 1
    if count_fail > 0:
        return jsonify("Effector Failed"), 400

    adaptation_status = True
    return jsonify("Effector Successful"), 200


@app.route("/return_to_previous", methods=["GET"])
def return_to_previous_state():
    global effector, device, current_status

    responses = []
    for result in results:
        if result[1] != "fail":
            write_log(f"Returning {result[0]} to {result[1]}...\n")
            responses.append(effector.execute(result[0], result[1]))

    return jsonify(responses)
