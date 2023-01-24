import os
import requests
from project import logging
from dotenv import load_dotenv

load_dotenv()


class PlanExecuteService:
    def plan(self, actions):
        for action in actions:
            device, action_type, body = action.split(":")
            response = requests.get(f"{os.getenv('SIMULATOR_HOST')}/{device}/status")
            if response.json()["status"] != "inactive":
                action_result = self.execute(device, action_type, body)
                logging.info(
                    f"Action performed on {device} and the result is {action_result}"
                )
                return device, response.json()["status"]
        logging.info(f"No device available to execute the actions specified")
        return device, "fail"

    def execute(self, device, action_type, body):
        if action_type == "STATUS":
            response = requests.post(
                f"{os.getenv('SIMULATOR_HOST')}/{device}/status",
                json={"new_status": body},
            )
        elif action_type == "MESSAGE":
            response = requests.post(
                f"{os.getenv('SIMULATOR_HOST')}/{device}/send_message",
                json={"type": "status", "body": body, "to": device},
            )
        if response.status_code == 200:
            return "success"
        return "fail"
