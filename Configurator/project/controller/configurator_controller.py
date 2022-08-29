from multiprocessing.dummy import Pool

import requests
from flask import jsonify, request
from project import app

devices = []


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure", methods=["POST"])
def configure():
    configuration = dict(request.json)
    pool = Pool(1)

    future_response = []

    future_response.append(pool)
    print(
        requests.post(
            "http://localhost:5001/configure",
            json={
                "devices": configuration["devices"],
                "exchange": configuration["communication"]["exchange"],
            },
        )
    )

    print(
        requests.post(
            "http://localhost:5002/configure",
            json={
                "communication": configuration["communication"],
                "scenarios": configuration["scenarios"],
            },
        )
    )

    print(
        requests.post(
            "http://localhost:5003/configure",
            json={
                "adaptation_strategies": configuration["adaptation_strategies"],
            },
        )
    )

    return jsonify("All things set!")
