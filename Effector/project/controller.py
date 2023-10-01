import os

from datetime import datetime
from dotenv import load_dotenv
from flask import jsonify, request
from project import app

from .effector import Effector
from .utils import write_log

effector = None
device, current_status = None, None
load_dotenv()
adaptation_status = False
results = []


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
    global effector, device, current_status, adaptation_status, results

    scenario = request.args.get("scenario")
    adapt_type = request.args.get("adapt_type")

    write_log(f"Applying {adapt_type} action for {scenario}.")
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
    global effector, device, current_status, results

    responses = []
    for result in results:
        if result[1] != "fail":
            if result[1] == "STATUS":
                write_log(f"Returning {result[0]} to {result[1]}...\n")
                result = effector.execute(result[0], result[1], result[2])
                responses.append(result)
                msg_log = f"Cautious adaptation result is {result}"
                write_log(msg_log)
                return jsonify(msg_log), 200
            else:
                write_log(
                    f"Not possible to apply cautious on adaptation action of the type {result[1]}\n"
                )
                return jsonify("error"), 400
