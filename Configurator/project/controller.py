import os
from multiprocessing.dummy import Pool

import requests
from datetime import datetime
from dotenv import load_dotenv
from flask import jsonify, request, send_file
from project import app

from .utils import write_log
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
    if os.path.exists(f"../{os.getenv('LOGS_PATH')}"):
        now = datetime.now()
        new_name = f"../{os.getenv('LOGS_PATH')}".replace(
            "logs", f"logs_{now.strftime('%d%m%Y%H%M')}"
        )
        os.rename(f"../{os.getenv('LOGS_PATH')}", new_name)
    configuration = dict(request.json)
    write_log(f"Starting {configuration['project']}...")
    errors_simulator = validate_simulator(configuration)

    # if errors_simulator:
    #     return jsonify(errors_simulator), 400

    errors_adapater = validate_adapter(configuration)

    if errors_adapater or errors_simulator:
        return (
            jsonify(
                {
                    "errors simulator modeling": errors_simulator,
                    "errors adapter modeling": errors_adapater,
                }
            ),
            400,
        )

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

        return jsonify(assert_scenario(configuration["scenarios"]))

    response = {}
    for key, value in result.items():
        response[key] = value.json()

    return jsonify(response), 400


@app.route("/validate_scenario", methods=["POST"])
def validate_scenario():
    return jsonify(assert_scenario(request.json))


@app.route("/get_logs", methods=["GET"])
def get_logs():
    return send_file(
        f'{os.getcwd().split("Configurator")[0]}{os.getenv("LOGS_PATH")}',
        as_attachment=True,
    )
