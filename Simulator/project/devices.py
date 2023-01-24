import os
from datetime import datetime

from dotenv import load_dotenv
from flask import jsonify

from .communication_service import CommunicationService
from .publisher import DevicePublisher
from .subscriber import DeviceSubscriber

load_dotenv()
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
        log_file = open(os.getenv("LOGS_PATH"), "a")

        if new_status in self.status:
            log_file.write(
                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {self.name} changed status from {self.current_status} to {new_status}\n"
            )
            self.current_status = new_status
            return jsonify({"received": new_status, "new status": self.current_status})

        log_file.close()
        return jsonify({"error": "Inexistent Status"})

    def create_queue_and_routes(self):
        CommunicationService
