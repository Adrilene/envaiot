from project import app
from flask import jsonify, request
from ..model.devices import Device
from ..utils.list_operations import get_current_device

devices = []


@app.route("/configure", methods=["POST"])
def configure():
    global devices
    # import ipdb

    # ipdb.set_trace()
    devices = []
    for device in request.json["devices"]:
        new_device = Device(
            device["name"],
            device["status"],
            device["senders"],
            request.json["exchange"],
        )

        devices.append(new_device)

    for device in devices:
        device.subscriber.start()

    return jsonify({"Devices instatiated": [device.name for device in devices]})


@app.route("/devices_list", methods=["GET"])
def get_devices_list():
    return jsonify(
        {
            "Devices instatiated": [
                f"{device.name} - {device.current_status}" for device in devices
            ]
        }
    )


@app.route("/<device_name>/status", methods=["GET", "POST"])
def status(device_name):
    global devices

    current_device = get_current_device(device_name)

    if not current_device:
        return jsonify({"Error": f"Device Not Found {device_name}"})

    if request.method == "GET":
        return current_device.get_status()

    new_status = dict(request.json)["new_status"]
    return current_device.set_status(new_status)


@app.route("/<device_name>/send_message", methods=["POST"])
def send_message(device_name):
    global devices

    current_device = get_current_device(device_name, devices)

    if not current_device:
        return jsonify({"Error": f"Device Not Found {device_name}"})

    return jsonify(
        current_device.publisher.publish(
            dict(request.json)["message"], device_name=device_name
        )
    )
