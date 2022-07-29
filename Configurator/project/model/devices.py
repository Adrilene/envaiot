from flask import jsonify
from project import app


class Device:
    def __init__(self, name, status):
        self.name = name
        self.status = status
        self.current_status = self.status[0]

    def get_status(self):
        return jsonify({"status": self.current_status})

    def set_status(self, new_status):
        if new_status in self.status:
            self.current_status = new_status
            return jsonify({"received": new_status, "new status": self.status})

        return jsonify({"error": "Inexistent Status"})
