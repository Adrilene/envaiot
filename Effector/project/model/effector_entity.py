import requests


class Effector:
    def __init__(self, adaptation_actions, return_to_normal_actions):
        self.adaptation_actions = adaptation_actions
        self.return_to_normal_actions = return_to_normal_actions

    def adapt(self, scenario):
        print('adapt: ', self.adaptation_actions[scenario])
        for step in self.adaptation_actions[scenario]:
            print("I'm adapting")
            print(f"STEP: {step}")
            requests.request(method=step["method"],
                             url=step["url"],
                             json=step["body"])

    def behave_normal(self, scenario):
        print('normal: ', self.return_to_normal_actions[scenario])
        for step in self.return_to_normal_actions[scenario]:
            print("I'm returning to normal")
            print(f"STEP: {step}")
            requests.request(method=step["method"],
                             url=step["url"],
                             json=step["body"])
