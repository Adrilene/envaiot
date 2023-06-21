from flask import jsonify, request
from project import app

from .devices import Device
from .string_operations import get_exchange_name
from .utils import get_current_device, write_log


@app.route("/configure", methods=["POST"])
def configure():
    global devices
    devices = []
    resources = request.json["resources"]
    exchange_name = get_exchange_name(request.json["project"])
    for device in resources.keys():
        status = resources[device]["status"] + ["active", "inactive"]
        senders = resources[device]["senders"]
        devices.append(Device(device, status, senders, exchange_name))

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

    current_device = get_current_device(device_name, devices)

    if not current_device:
        return jsonify({"Error": f"Device Not Found {device_name}"}), 400

    if request.method == "GET":
        return current_device.get_status()

    if dict(request.json)["new_status"] not in current_device.status:
        return jsonify(f"Status not available for device {current_device}"), 400

    new_status = dict(request.json)["new_status"]
    return current_device.set_status(new_status)


@app.route("/<device_name>/send_message", methods=["POST"])
def send_message(device_name):
    global devices
    current_device = get_current_device(device_name, devices)
    if "to" in dict(request.json).keys():
        recipient_device = get_current_device(dict(request.json)["to"], devices)
        if not recipient_device:
            return jsonify({"Error": f"Device Not Found {device_name}"}), 400

    if not current_device:
        return jsonify({"Error": f"Device Not Found {device_name}"}), 400

    message = {"type": dict(request.json)["type"], "body": dict(request.json)["body"]}
    if not "to" in dict(request.json).keys():
        write_log(f"{device_name} published {message}")
    else:
        write_log(f"{device_name} sent {message} to {request.json['to']}.")

    return jsonify(
        current_device.publisher.publish(
            message,
            device_name=device_name,
            recipient=dict(request.json)["to"]
            if "to" in dict(request.json).keys()
            else None,
        )
    )
