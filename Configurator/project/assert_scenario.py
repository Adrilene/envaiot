import os
from time import sleep

import requests
from dotenv import load_dotenv

from .utils import write_log

load_dotenv()


def analyse_result():
    last_lines = []
    with open(f"../{os.getenv('LOGS_PATH')}", "r") as f:
        lines = f.readlines()
        last_lines.append("success" in lines[-1])
        last_lines.append("success" in lines[-2])
        last_lines.append("success" in lines[-3])
        if True in last_lines:
            return 200
        return 400


def send_message(scenario):
    results = []
    message = scenario
    message["body"] = scenario["body"] if "body" in scenario.keys() else ""
    if "receiver" in scenario:
        message["to"] = scenario["receiver"]
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

    return results


def assert_scenario(scenarios):
    msg = []
    for scenario_name in scenarios["adaptation"].keys():
        results = []
        count = 1
        write_log(f"Asserting scenario {scenario_name}...")

        for scenario in scenarios["adaptation"][scenario_name]["scenario"]:
            results.extend(send_message(scenario))
            count += 1
            sleep(count + 1)

        sleep(3)

        results.append(analyse_result())

        result = ""

        if results.count(200) == len(results):
            if scenarios["adaptation"][scenario_name]["cautious"]:
                for scenario in scenarios["normal"]:
                    results.extend(send_message(scenario))
                sleep(3)
                result = analyse_result()
                if result == 200:
                    result = f"[SUCCESS] Scenario {scenario_name} passed and the cautious adaptation was applied."
                else:
                    result = f"[SUCCESS] Scenario {scenario_name} passed and the cautious adaptation was not applied."

            else:
                result = f"[SUCCESS] Scenario {scenario_name} passed."
        else:
            result = f"[FAILED] Scenario {scenario_name} failed."

        write_log(result)
        msg.append(result)

    return msg
