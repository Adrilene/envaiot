import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


class PlanExecuteService:
    def plan(self, actions):
        log_file = open(os.getenv("LOGS_PATH"), "a")

        for action in actions:
            device, action_type, body = action.split(":")
            response = requests.get(f"{os.getenv('SIMULATOR_HOST')}/{device}/status")
            log_file.write(
                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {device} status is {response.json()['status']}\n"
            )
            
            if response.json()["status"] != "inactive":
                action_result = self.execute(device, action_type, body)
                log_file.write(
                    f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Action performed on {device} and the result is {action_result}\n"
                )
                return device, response.json()["status"]
        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - No device available to execute the actions specified\n"
        )

        log_file.close()
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
