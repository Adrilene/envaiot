import os
import requests
from dotenv import load_dotenv
from termcolor import colored
from time import sleep


load_dotenv()


def assert_scenario(adaptation_scenarios, exchange):
    for scenario_name in adaptation_scenarios.keys():
        results = []
        print(f"Asserting scenario {scenario_name}")
        for scenario in adaptation_scenarios[scenario_name]:
            message = scenario
            if "receiver" in scenario:
                message["to"] = scenario["receiver"]
                message["body"] = ""
                receiver = message.pop("receiver")
                results.append(
                    requests.post(
                        f"{os.getenv('SIMULATOR_HOST')}/{receiver}/send_message",
                        json=message,
                    ).status_code
                )
            elif "sender" in scenario:
                sender = message.pop("sender")
                results.append(
                    requests.post(
                        f"{os.getenv('SIMULATOR_HOST')}/{sender}/send_message",
                        json=message,
                    ).status_code
                )
            sleep(1)

        if results.count(200) == len(results):
            print(colored(f"[SUCCESS] Scenario {scenario_name} passed.", "green"))
        else:
            print(colored(f"[FAILED] Scenario {scenario_name} failed.", "red"))
