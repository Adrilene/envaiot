from project.entity.observer_broker import ObserverBroker
from project.entity.observer_middleware import ObserverMiddleware
from flask import jsonify, request
from project import app
from time import sleep
import socketio
import requests
import json


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/start", methods=["POST"])
def start():
    global obs_mw
    if request.json["interface_type"] == "observer":
        ObserverBroker(request.json).start()

    if request.json["interface_type"] == "middleware":
        ObserverMiddleware(request.json).start()

    return jsonify({"msg": "Observer Start"})
