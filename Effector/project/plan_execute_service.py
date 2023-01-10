import os
import requests
from dotenv import load_dotenv

load_dotenv()
class PlanExecuteService:
    def plan(self, actions):
        for action in actions:
            device, status = action.split(":")
            print("-----------")
            print(f"{device} - {status}")
            print("-----------")
            response = requests.get(f"{os.getenv('SIMULATOR_HOST')}/{device}/status")
            if response.json()["status"] == "active":
                action_result = self.execute(device, status)
                print(f"Action performed on {device} and the result is {action_result}")
                return device, response.json()["status"]
        print(f"No device available to execute the actions specified")
        return device, "fail"

    def execute(self, device, status):
        response = requests.post(
            f"{os.getenv('SIMULATOR_HOST')}/{device}/status", json={"new_status": status}
        )
        if response.status_code == 200:
            return "success"
        return "fail"
