import os

from datetime import datetime
from dotenv import load_dotenv
from flask import jsonify, request
from project import app

from .effector import Effector

effector = None
device, curent_status = None, None
load_dotenv()


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
    global effector, device, current_status

    log_file = open(os.getenv("LOGS_PATH"), "a")
    scenario = request.args.get("scenario")
    adapt_type = request.args.get("adapt_type")

    log_file.write(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Adapting {adapt_type} for {scenario}\n")

    device, current_status = effector.adapt(scenario, adapt_type)
    if current_status == "fail":
        return jsonify("Effector Failed"), 500

    log_file.close()
    return jsonify("Effector Successful"), 200


@app.route("/return_to_previous", methods=["GET"])
def return_to_previous_state():
    global effector, device, current_status

    log_file = open(os.getenv("LOGS_PATH"), "a")

    log_file.write(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Returning {device} to {current_status}...\n")
    response = effector.execute(device, current_status)

    if response == "success":
        return jsonify("Returned to previous state")

    return jsonify("Failed when returning to previous state"), 500
