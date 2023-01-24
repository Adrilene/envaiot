import os
from datetime import datetime
from multiprocessing.dummy import Pool
from time import sleep

import requests
from dotenv import load_dotenv
from flask import jsonify, request, send_file
from project import app

from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator

devices = []


load_dotenv()


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure_simulator", methods=["POST"])
def configure_simulator():
    log_file = open(os.getenv("LOGS_PATH"), "a")

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
        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Simulator configurated with:\n"
        )
        log_file.write(f"{configuration}\n")
        return jsonify("Simulator set!")

    log_file.close()
    return result


@app.route("/configure_adapter", methods=["POST"])
def configure_adapter():
    log_file = open(os.getenv("LOGS_PATH"), "a")
    configuration = dict(request.json)
    print(f"Starting {configuration['project']}...")
    errors = validate_adapter(configuration)
    if errors:
        return jsonify(errors), 400

    log_file.write(
        f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Modelling is correct. Starting to configure adapter...\n"
    )

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
        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Adapter configurated with:\n"
        )
        log_file.write(f"Observer: {observer_configuration}\n")
        log_file.write(f"Effector {effector_configuration}\n")
        return jsonify("Adapter set!")

    response = {}
    for key, value in result.items():
        response[key] = value.json()

    log_file.close()
    return jsonify(response), 400


@app.route("/configure_all", methods=["POST"])
def configure_all():
    log_file = open(os.getenv("LOGS_PATH"), "a")

    configuration = dict(request.json)
    log_file.write(
        f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Starting {configuration['project']}...\n"
    )
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

        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Components configured\n"
        )
        log_file.write(f"Simulator: {simulator_configuration}\n")
        log_file.write(f"Obsever: {observer_configuration}\n")
        log_file.write(f"Effector: {effector_configuration}\n")
        return jsonify("All things set!")

    response = {}
    for key, value in result.items():
        response[key] = value.json()

    log_file.close()
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

    return send_file(os.getenv("LOGS_PATH"), as_attachment=True)
