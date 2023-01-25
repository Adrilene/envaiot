import json
import os
from copy import deepcopy
from datetime import datetime
from threading import Thread

import requests
from dotenv import load_dotenv

from .communication_service import CommunicationService
from .connection import subscribe_in_all_queues
from .monitor_analyse_service import MonitorAnalyseService
from .util_operations import (
    get_exchange_name,
    get_receiver_routing_key,
    get_scenario,
    get_sender_routing_key,
)

scenarios_sequence = []
adaptation_scenario = ""
has_adapted = False
has_adapted_uncertainty = False

load_dotenv()


class Observer(CommunicationService, MonitorAnalyseService, Thread):
    def __init__(self, communication, scenarios, project_name):
        global scenarios_sequence, adaptation_scenario, has_adapted, has_adapted_uncertainty
        #Resetting global variables
        scenarios_sequence = []
        adaptation_scenario = ""
        has_adapted = False
        has_adapted_uncertainty = False

        CommunicationService.__init__(self, get_exchange_name(project_name))
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
        log_file = open(os.getenv("LOGS_PATH"), "a")

        data = json.loads(data.decode("UTF-8"))
        current_scenario = get_scenario(data, method.routing_key)

        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Observer received: {data} from {method.routing_key}\n"
        )

        if self.analyse_normal_scenario(current_scenario, self.scenarios["normal"]):
            if has_adapted or has_adapted_uncertainty:
                log_file.write(
                    f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Adaptation worked successfully.\n"
                )
                has_adapted = False
                has_adapted_uncertainty = False
                scenarios_sequence = []
            log_file.write(
                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - System is under a normal scenario.\n"
            )
        else:
            scenarios_sequence.append(current_scenario)
            adaptation = self.analyse_adaptation_scenario(
                scenarios_sequence, self.scenarios["adaptation"]
            )
            if adaptation != "wait" and adaptation != False:
                if adaptation != "uncertainty":
                    log_file.write(
                        f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Scenario {adaptation} detected.\n"
                    )
                    adaptation_scenario = adaptation
                    response = requests.get(
                        f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={adaptation_scenario}&adapt_type=adaptation"
                    )
                    has_adapted = True
                    if response.status_code == 200:
                        log_file.write(
                            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Adapted for {adaptation_scenario}\n"
                        )
                    else:
                        log_file.write(
                            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Uncertainty detected for {adaptation_scenario}\n"
                        )
                        response = requests.get(
                            f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={adaptation_scenario}&adapt_type=uncertainty"
                        )
                        has_adapted_uncertainty = True
                        scenarios_sequence = []
                        if response.status_code == 200:
                            log_file.write(
                                f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Adapted uncertainty for {adaptation_scenario}\n"
                            )

                else:
                    log_file.write(
                        f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Uncertainty detected for {adaptation_scenario}\n"
                    )
                    response = requests.get(
                        f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={adaptation_scenario}&adapt_type=uncertainty"
                    )
                    has_adapted_uncertainty = True
                    if response.status_code == 200:
                        log_file.write(
                            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - Adapted uncertainty for {adaptation_scenario}\n"
                        )
                    scenarios_sequence = []

        log_file.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_scenarios(self, scenarios):
        new_scenarios = deepcopy(scenarios)
        for key, value in scenarios.items():
            if key == "normal":
                if "receiver" in value.keys():
                    new_message[key]["topic"] = get_receiver_routing_key(
                        new_scenarios[key]["receiver"]
                    )
                    new_scenarios[key].pop("receiver")
                if "sender" in value.keys():
                    new_scenarios[key]["topic"] = get_sender_routing_key(
                        new_scenarios[key]["sender"]
                    )
                    new_scenarios[key].pop("sender")

                new_message = new_scenarios[key]
                new_scenarios[key] = [new_message]

            elif key == "adaptation":
                for scenario_name in value.keys():
                    new_scenarios["adaptation"][scenario_name] = []
                    for message in value[scenario_name]:
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
                        new_scenarios["adaptation"][scenario_name].append(new_message)
        return new_scenarios
