import json
import os
from copy import deepcopy
from threading import Thread
from time import sleep

import requests
from dotenv import load_dotenv

from .communication_service import CommunicationService
from .connection import subscribe_in_all_queues
from .monitor_analyse_service import MonitorAnalyseService
from .utils import (
    get_exchange_name,
    get_receiver_routing_key,
    get_scenario,
    get_sender_routing_key,
    write_log,
)

scenarios_sequence = []
adaptation_scenario = ""
has_adapted = False
has_adapted_uncertainty = False

load_dotenv()


class Observer(CommunicationService, MonitorAnalyseService, Thread):
    def __init__(self, communication, scenarios, project_name):
        global scenarios_sequence, adaptation_scenario, has_adapted, has_adapted_uncertainty
        # Resetting global variables
        scenarios_sequence = []
        adaptation_scenario = ""
        has_adapted = False
        has_adapted_uncertainty = False

        CommunicationService.__init__(
            self, get_exchange_name(project_name), communication["host"]
        )
        Thread.__init__(self)
        self.scenarios = self.get_scenarios(scenarios)
        self.queue = "observer"
        self.declare_queue(self.queue)
        subscribe_in_all_queues(
            communication["host"],
            communication["user"],
            communication["password"],
            get_exchange_name(project_name),
            self.queue,
            self.channel,
        )

    def run(self):
        print(f"[*] Starting Observer")
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
            auto_ack=False,
        )
        self.channel.start_consuming()

    def callback(self, ch, method, properties, data):
        global scenarios_sequence, has_adapted, has_adapted_uncertainty, adaptation_scenario

        data = json.loads(data.decode("UTF-8"))
        current_scenario = get_scenario(data, method.routing_key)

        write_log(f"Observer received: {data} from {method.routing_key}.")

        scenarios_sequence.append(current_scenario)
        analysis_normal = self.analyse_normal_scenario(
            scenarios_sequence, self.scenarios["normal"]
        )

        if analysis_normal == True:
            write_log(f"System is under a normal scenario.")
            if has_adapted or has_adapted_uncertainty:
                if self.scenarios["adaptation"][adaptation_scenario]["cautious"]:
                    write_log(f"Resetting to previous state")
                    response = requests.get(
                        f"{os.getenv('EFFECTOR_HOST')}/return_to_previous"
                    )
                    if response.status_code == 200:
                        write_log("Resource reset successfully")
                    else:
                        write_log(response.json()[0])
            self.reset_values()
        elif analysis_normal == "wait":
            pass
        else:
            adaptation = self.analyse_adaptation_scenario(
                scenarios_sequence, self.scenarios["adaptation"]
            )
            print(f"SCENARIOS: {scenarios_sequence}")
            print(f"ADAPTATION RESULT: {adaptation}")
            if adaptation in self.scenarios["adaptation"].keys():
                if adaptation != "uncertainty":
                    write_log(f"Scenario {adaptation} detected.")
                    adaptation_scenario = adaptation
                    response = requests.get(
                        f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={adaptation_scenario}&adapt_type=adaptation"
                    )
                    has_adapted = True
                    if response.status_code == 200:
                        write_log(f"Adapted for {adaptation_scenario} successfully.")
                        scenarios_sequence = []

                    else:
                        msg_log = f"Adaptation failed for {adaptation_scenario}. Adapting uncertainty..."
                        write_log(msg_log)
                        response = requests.get(
                            f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={adaptation_scenario}&adapt_type=uncertainty"
                        )
                        scenarios_sequence = []
                        has_adapted_uncertainty = True
                        if response.status_code == 200:
                            write_log(
                                f"Adapted uncertainty for {adaptation_scenario} successfully."
                            )
                            scenarios_sequence = []

                        else:
                            msg_log = f"Uncertainty for {adaptation_scenario} failed."
                            write_log(msg_log)

            elif adaptation == None:
                scenarios_sequence = []

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def reset_values(self):
        global has_adapted, has_adapted_uncertainty, scenarios_sequence, adaptation_scenario

        has_adapted, has_adapted_uncertainty = False, False
        scenarios_sequence = []

    def get_scenarios(self, scenarios):
        new_scenarios = deepcopy(scenarios)
        for key, value in scenarios.items():
            if key == "normal":
                new_scenarios["normal"] = []
                for message in scenarios[key]:
                    new_message = deepcopy(message)
                    if "receiver" in message.keys():
                        new_message["topic"] = get_receiver_routing_key(
                            message["receiver"]
                        )
                        new_message.pop("receiver")
                    if "sender" in message.keys():
                        new_message["topic"] = get_sender_routing_key(message["sender"])
                        new_message.pop("sender")

                    new_message["body"] = (
                        message["body"] if "body" in message.keys() else ""
                    )

                    new_scenarios["normal"].append(new_message)
            elif key == "adaptation":
                for scenario_name in value.keys():
                    new_scenarios["adaptation"][scenario_name]["cautious"] = scenarios[
                        "adaptation"
                    ][scenario_name]["cautious"]
                    new_scenarios["adaptation"][scenario_name]["scenario"] = []
                    for message in value[scenario_name]["scenario"]:
                        new_message = deepcopy(message)
                        if "receiver" in message.keys():
                            new_message["topic"] = get_receiver_routing_key(
                                message["receiver"]
                            )
                            new_message.pop("receiver")
                        if "sender" in message.keys():
                            new_message["topic"] = get_sender_routing_key(
                                message["sender"]
                            )
                            new_message.pop("sender")
                        new_message["body"] = (
                            message["body"] if "body" in message.keys() else ""
                        )
                        new_scenarios["adaptation"][scenario_name]["scenario"].append(
                            new_message
                        )

        return new_scenarios
