import requests


class PlanExecuteService:
    def plan(self, actions):
        for action in actions:
            device, status = action.split(":")
            response = requests.get(f"http://localhost:5001/{device}/status")
            if response.json()["status"] == "active":
                action_result = self.execute(device, status)
                print(f"Action performed on {device} and the result is {action_result}")
                return device, response.json()["status"]
            print(f"No device available to execute the actions specified")
            return device, "fail"

    def execute(self, device, status):
        response = requests.post(
            f"http://localhost:5001/{device}/status", json={"new_status": status}
        )
        if response.status_code == 200:
            return "success"
        return "fail"
