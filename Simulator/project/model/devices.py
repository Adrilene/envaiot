from flask import jsonify
from ..utils.string_operations import (
    get_publishing_routing_key,
    get_subscribing_routing_key,
)

from .device_publisher import DevicePublisher
from .device_subscriber import DeviceSubscriber
from ..service.communication_service import CommunicationService


class Device:
    def __init__(self, name, status, senders, exchange):
        self.name = name
        self.status = status
        self.current_status = self.status[0]
        self.publisher = DevicePublisher(exchange, self.name)
        self.subscriber = DeviceSubscriber(exchange, self.name, senders)

    def get_status(self):
        return jsonify({"status": self.current_status})

    def set_status(self, new_status):
        if new_status in self.status:
            self.current_status = new_status
            return jsonify({"received": new_status, "new status": self.current_status})

        return jsonify({"error": "Inexistent Status"})

    def create_queue_and_routes(self):
        CommunicationService
