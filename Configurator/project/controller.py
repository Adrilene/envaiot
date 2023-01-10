from multiprocessing.dummy import Pool

from flask import jsonify, request, make_response
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
    print(f"Starting {configuration['project']}...")
    errors = validate_simulator(configuration)
    if (errors):
        return jsonify(errors), 400

    print("Modelling is correct. Starting to configure simulator...")
    result = request_simulator(configuration)
    if result.status_code == 200:
        return jsonify("Simulator set!")
    return result


@app.route("/configure_adapter", methods=["POST"])
def configure_adapter():
    configuration = dict(request.json)
    print(f"Starting {configuration['project']}...")
    errors = validate_adapter(configuration)
    if (errors):
        return jsonify(errors), 400

    print("Modelling is correct. Starting to configure adapter...")
    result = {}
    result["Observer"] = request_observer(
        {   
            "project": configuration['project'],
            "communication": configuration["communication"],
            "scenarios": configuration["scenarios"],
        }
    )
    
    result["Effector"] = request_effector(
        {
            "strategies": configuration["strategies"],
        }
    )
    
    if result["Observer"].status_code == 200 and result["Effector"].status_code == 200:
        return jsonify("Adapter set!")    
    
    response = {}
    for key, value in result.items():
        response[key] = value.json()
    return jsonify(response), 400



@app.route("/configure_all", methods=["POST"])
def configure_all():
    configuration = dict(request.json)
    print(f"Starting {configuration['project']}...")
    pool = Pool(1)

    future_response = []

    future_response.append(pool)
    result = {}
    result["Simulator"] = request_simulator(
        {
            "project": configuration["project"],
            "resources": configuration["resources"],
            "communication": configuration["communication"]
        }
    )


    result["Observer"] = request_observer(
        {   
            "project": configuration["project"],
            "communication": configuration["communication"],
            "scenarios": configuration["scenarios"],
        }
    )
    

    result["Effector"] = request_effector(
        {
            "strategies": configuration["strategies"],
        }
    )
    
    if result["Simulator"].status_code == 200 and result["Observer"].status_code == 200 and result["Effector"].status_code == 200:
        return jsonify("All things set!")
    
    response = {}
    for key, value in result.items():
        response[key] = value.json()
    return jsonify(response), 400
