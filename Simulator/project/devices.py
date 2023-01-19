from flask import jsonify
from project import logging
from .publisher import DevicePublisher
from .subscriber import DeviceSubscriber
from .communication_service import CommunicationService

class Device:
    def __init__(self, name, status, senders, exchange):
        self.name = name
        self.status = status
        self.current_status = self.status[0]
        self.publisher = DevicePublisher(exchange, name)
        self.subscriber = DeviceSubscriber(exchange, name, senders)

    def get_status(self):
        return jsonify({"status": self.current_status})

    def set_status(self, new_status):
        if new_status in self.status:
            logging.info(f"{self.name} changed status from {self.current_status} to {new_status}")
            self.current_status = new_status
            return jsonify({"received": new_status, "new status": self.current_status})

        return jsonify({"error": "Inexistent Status"})

    def create_queue_and_routes(self):
        CommunicationService
