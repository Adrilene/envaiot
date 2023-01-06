from multiprocessing.dummy import Pool

from flask import jsonify, request
from project import app
from .requests import request_simulator, request_observer, request_effector
from .validator_simulator import validate_simulator
from .validator_adapter import validate_adapter

devices = []


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure_simulator", methods=["POST"])
def configure_simulator():
    configuration = dict(request.json)
    errors = validate_simulator(configuration)
    if (errors):
        return jsonify(errors), 400

    print("Modelling is correct. Starting to configure simulator...")
    print(
        request_simulator(configuration)
    )
    return jsonify("Simulator set!")


@app.route("/configure_adapter", methods=["POST"])
def configure_adapter():
    configuration = dict(request.json)
    errors = validate_adapter(configuration)
    if (errors):
        return jsonify(errors), 400

    print("Modelling is correct. Starting to configure adapter...")
    
    print(
        request_observer(
            {
                "communication": configuration["communication"],
                "scenarios": configuration["scenarios"],
            }
        )
    )

    print(
        request_effector(
            {
                "strategies": configuration["strategies"],
            }
        )
    )


    return jsonify("Adapter set!")    


@app.route("/configure_all", methods=["POST"])
def configure_all():
    configuration = dict(request.json)
    pool = Pool(1)

    future_response = []

    future_response.append(pool)
    print(
        request_simulator(
            {
                "devices": configuration["devices"],
                "exchange": configuration["communication"]["exchange"]
            }
        )
    )

    print(
        request_observer(
            {
                "communication": configuration["communication"],
                "scenarios": configuration["scenarios"],
            }
        )
    )

    print(
        request_effector(
            {
                "adaptation_strategies": configuration["adaptation_strategies"],
            }
        )
    )

    return jsonify("All things set!")
