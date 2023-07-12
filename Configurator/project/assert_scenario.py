import os
from time import sleep

import requests
from dotenv import load_dotenv

from .utils import write_log

load_dotenv()


def assert_scenario(adaptation_scenarios):
    msg = []
    for scenario_name in adaptation_scenarios.keys():
        results = []
        write_log(f"Asserting scenario {scenario_name}...")
        for scenario in adaptation_scenarios[scenario_name]:
            message = scenario
            if "receiver" in scenario:
                message["to"] = scenario["receiver"]
                message["body"] = scenario["body"] if scenario["body"] else ""
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
            sleep(len(adaptation_scenarios[scenario_name]))

        results.append(
            requests.get(
                f"{os.getenv('OBSERVER_HOST')}/get_adaptation_status"
            ).status_code
        )

        result = ""
        if results.count(200) == len(results):
            result = f"[SUCCESS] Scenario {scenario_name} passed."
        else:
            result = f"[FAILED] Scenario {scenario_name} failed."

        write_log(result)
        msg.append(result)

    return msg
