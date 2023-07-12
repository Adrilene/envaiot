import os
from multiprocessing.dummy import Pool
from time import sleep

import requests
from dotenv import load_dotenv
from flask import jsonify, request, send_file
from project import app

from .utils import write_log, get_exchange_name
from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator
from .assert_scenario import assert_scenario

devices = []


load_dotenv()


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure_simulator", methods=["POST"])
def configure_simulator():
    configuration = dict(request.json)
    print(f"Starting {configuration['project']}...")
    errors = validate_simulator(configuration)
    if errors:
        return jsonify(errors), 400

    print("Modelling is correct. Starting to configure simulator...")
    result = requests.post(
        f"{os.getenv('SIMULATOR_HOST')}/configure", json=configuration
    )
    if result.status_code == 200:
        write_log(f"Simulator configurated with:")
        write_log(f"{configuration}\n")
        return jsonify("Simulator set!")

    return result


@app.route("/configure_adapter", methods=["POST"])
def configure_adapter():
    configuration = dict(request.json)
    print(f"Starting {configuration['project']}...")
    errors = validate_adapter(configuration)
    if errors:
        return jsonify(errors), 400

    write_log(f"Modelling is correct. Starting to configure adapter...")

    result = {}
    observer_configuration = {
        "project": configuration["project"],
        "communication": configuration["communication"],
        "scenarios": configuration["scenarios"],
    }
    effector_configuration = {
        "strategies": configuration["strategies"],
    }
    result["Observer"] = requests.post(
        f"{os.getenv('OBSERVER_HOST')}/configure",
        json=observer_configuration,
    )
    result["Effector"] = requests.post(
        f"{os.getenv('EFFECTOR_HOST')}/configure",
        json=effector_configuration,
    )

    if result["Observer"].status_code == 200 and result["Effector"].status_code == 200:
        write_log(f"Adapter configurated with:")
        write_log(f"Observer: {observer_configuration}")
        write_log(f"Effector {effector_configuration}")
        return jsonify("Adapter set!")

    response = {}
    for key, value in result.items():
        response[key] = value.json()

    return jsonify(response), 400


@app.route("/configure_all", methods=["POST"])
def configure_all():
    configuration = dict(request.json)
    write_log(f"Starting {configuration['project']}...")
    pool = Pool(1)

    future_response = []

    future_response.append(pool)
    result = {}
    simulator_configuration = {
        "project": configuration["project"],
        "resources": configuration["resources"],
        "communication": configuration["communication"],
    }
    result["Simulator"] = requests.post(
        f"{os.getenv('SIMULATOR_HOST')}/configure",
        json=simulator_configuration,
    )

    observer_configuration = {
        "project": configuration["project"],
        "communication": configuration["communication"],
        "scenarios": configuration["scenarios"],
    }
    result["Observer"] = requests.post(
        f"{os.getenv('OBSERVER_HOST')}/configure",
        json=observer_configuration,
    )

    effector_configuration = {
        "strategies": configuration["strategies"],
    }
    result["Effector"] = requests.post(
        f"{os.getenv('EFFECTOR_HOST')}/configure",
        json=effector_configuration,
    )

    if (
        result["Simulator"].status_code == 200
        and result["Observer"].status_code == 200
        and result["Effector"].status_code == 200
    ):
        write_log(f"Components configured:")
        write_log(f"Simulator: {simulator_configuration}")
        write_log(f"Obsever: {observer_configuration}")
        write_log(f"Effector: {effector_configuration}")

        return jsonify(assert_scenario(configuration["scenarios"]["adaptation"]))

    response = {}
    for key, value in result.items():
        response[key] = value.json()

    return jsonify(response), 400


@app.route("/validate_scenario", methods=["POST"])
def validate_scenario():
    scenarios = list(request.json)
    for scenario in scenarios:
        requests.post(
            f"{os.getenv('SIMULATOR_HOST')}/{scenario['from']}/send_message",
            json=scenario["message"],
        )

        sleep(2)

    return send_file(f'../{os.getenv("LOGS_PATH")}', as_attachment=True)


@app.route("/get_logs", methods=["GET"])
def get_logs():
    return send_file(f'{os.getenv("LOGS_PATH")}', as_attachment=True)
