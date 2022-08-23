from ..model.observer import Observer
from flask import jsonify, request
from project import app
from time import sleep
import socketio
import requests
import json


@app.route("/start", methods=["POST"])
def start():
    observer = Observer()

    return jsonify({"msg": "Observer Start"})
