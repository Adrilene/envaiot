import os
import json
from threading import Thread
from dotenv import load_dotenv
from copy import deepcopy

import requests
from project import logging

from .communication_service import CommunicationService
from .connection import subscribe_in_all_queues
from .monitor_analyse_service import MonitorAnalyseService
from .util_operations import (
    get_sender_routing_key,
    get_receiver_routing_key,
    get_exchange_name,
    get_scenario,
)

scenarios = []
adaptation = ''
has_adapted = False
has_adapted_uncertainty = False

load_dotenv()


class Observer(CommunicationService, MonitorAnalyseService, Thread):
    def __init__(self, communication, scenarios, project_name):
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
        global scenarios, has_adapted, has_adapted_uncertainty, adaptation
        ch.basic_ack(delivery_tag=method.delivery_tag)
        data = json.loads(data.decode("UTF-8"))
        current_scenario = get_scenario(data, method.routing_key)
        # scenarios.append(get_scenario(data, method.routing_key))

        logging.info(f"Observer received: {data} from {method.routing_key}")

        if self.analyse_normal_scenario(current_scenario, self.scenarios["normal"]):
            if has_adapted:
                logging.info(
                    "Adaptation worked. Returning affected devices to previous state..."
                )
                response = requests.get(
                    f"{os.getenv('EFFECTOR_HOST')}/return_to_previous"
                )
                scenarios = []
                has_adapted = False
                has_adapted_uncertainty = False

            elif has_adapted_uncertainty:
                logging.info("Adaptation for uncertainty worked.")
                scenarios = []
                has_adapted = False
                has_adapted_uncertainty = False
            else:
                logging.info("System is on normal scenario.")
            
        else:
            if has_adapted:
                logging.info("Adaptation failed. System is under an uncertainty scenario.")
                response = requests.get(
                    f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={adaptation}&adapt_type=uncertainty"
                )
            
            else:
                scenarios.append(current_scenario)
                adaptation = self.analyse_adaptation_scenario(
                    scenarios, self.scenarios["adaptation"]
                )
            
                if adaptation == False or adaptation == "wait":
                    logging.info("No adaptation scenario detected.")

                
                elif adaptation in self.scenarios["adaptation"].keys() and not has_adapted:
                    logging.info(
                        f"Adaptation scenario {adaptation} is occurring. Calling adaptation..."
                    )
                    response = requests.get(
                        f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={adaptation}&adapt_type=adaptation"
                    )
                    has_adapted = adaptation
                    if response.status_code == 200:
                        scenarios = []

                elif adaptation == "uncertainty" and has_adapted:
                    logging.info(
                        f"Uncertainty scenario {adaptation} is occurring. Calling adaptation..."
                    )
                    response = requests.get(
                        f"{os.getenv('EFFECTOR_HOST')}/adapt?scenario={has_adapted}&adapt_type=uncertainty"
                    )
                    has_adapted_uncertainty = True
                    scenarios = []

    def get_scenarios(self, scenarios):
        new_scenarios = deepcopy(scenarios)
        for key, value in scenarios.items():
            if key == "normal":
                if "receiver" in value.keys():
                    new_scenarios[key]["topic"] = get_receiver_routing_key(
                        new_scenarios[key]["receiver"]
                    )
                    new_scenarios[key].pop("receiver")
                if "sender" in value.keys():
                    new_scenarios[key]["topic"] = get_sender_routing_key(
                        new_scenarios[key]["sender"]
                    )
                    new_scenarios[key].pop("sender")

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
        
        print(new_scenarios)
        return new_scenarios
