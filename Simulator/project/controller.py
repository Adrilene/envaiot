import os
from datetime import datetime

from dotenv import load_dotenv
from flask import jsonify, request
from project import app

from .devices import Device
from .list_operations import get_current_device
from .string_operations import get_exchange_name

load_dotenv()
@app.route("/configure", methods=["POST"])
def configure():
    global devices
    devices = []
    resources = request.json["resources"]
    for device in resources.keys():
        status = resources[device]["status"] + ["active", "inactive"]
        senders = resources[device]["senders"]
        devices.append(
            Device(device, status, senders, get_exchange_name(request.json["project"]))
        )

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

    new_status = dict(request.json)["new_status"]
    return current_device.set_status(new_status)


@app.route("/<device_name>/send_message", methods=["POST"])
def send_message(device_name):
    global devices

    log_file = open(os.getenv("LOGS_PATH"), "a")

    current_device = get_current_device(device_name, devices)
    if "to" in dict(request.json).keys():
        recipient_device = get_current_device(dict(request.json)["to"], devices)
        if not recipient_device:
            return jsonify({"Error": f"Device Not Found {device_name}"}), 400

    if not current_device:
        return jsonify({"Error": f"Device Not Found {device_name}"}), 400

    message = {"type": dict(request.json)["type"], "body": dict(request.json)["body"]}
    if not "to" in dict(request.json).keys():
        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {device_name} published {message}\n"
        )
    else:
        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {device_name} sent {message} to {request.json['to']}\n"
        )

    log_file.close()
    return jsonify(
        current_device.publisher.publish(
            message,
            device_name=device_name,
            recipient=dict(request.json)["to"]
            if "to" in dict(request.json).keys()
            else None,
        )
    )
