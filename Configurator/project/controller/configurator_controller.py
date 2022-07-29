from project import app
from flask import jsonify, request
from ..model.devices import Device

devices = []


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure", methods=["POST"])
def configure():
    global devices
    for device in request.json:
        devices.append(
            Device(
                device["name"],
                device["status"],
            )
        )

    return jsonify({"Devices instatiated": [device.name for device in devices]})


@app.route("/devices_list", methods=["GET"])
def get_devices_list():
    return jsonify({"Devices instatiated": [device.name for device in devices]})


@app.route("/<device_name>/status", methods=["GET", "POST"])
def status(device_name, new_status=None):
    global devices

    current_device = None
    for device in devices:
        if device.name == device_name:
            current_device = device
    print(current_device)

    if not current_device:
        return jsonify({"Error": f"Device Not Found {device_name}"})

    if request.method == "GET":
        return current_device.get_status()

    return current_device.set_status(new_status)


def data_config_observer(request_json: dict):
    return {
        "interface_type": request_json["interface_type"],
        "connection_config": request_json["connection_config"],
        "normal_scenario": request_json["normal_scenario"],
        "exceptional_scenario": request_json["exceptional_scenario"],
    }


def data_config_effector(request_json: dict):
    return {
        "adaptation_actions": request_json["adaptation_actions"],
        "return_to_normal_actions": request_json["return_to_normal_actions"],
    }
