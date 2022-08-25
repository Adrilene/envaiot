import json
from threading import Thread

from ..service.communication_service import CommunicationService
from ..service.monitor_analyze_service import MonitorAnalyzeService
from ..util.connection import subscribe_in_all_queues

received_messages = []
received_topics = []


class Observer(CommunicationService, MonitorAnalyzeService, Thread):
    def __init__(self, communication, scenarios):
        CommunicationService.__init__(self, communication["exchange"])
        Thread.__init__(self)
        self.scenarios = scenarios
        self.queue = "observer"
        self.declare_queue(self.queue)
        subscribe_in_all_queues(
            communication["host"],
            communication["user"],
            communication["password"],
            communication["exchange"],
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
        global received_messages, received_topics
        ch.basic_ack(delivery_tag=method.delivery_tag)
        data = json.loads(data.decode("UTF-8"))
        received_messages.append(data)
        received_topics.append(method.routing_key)
        print(f"RECEIVED: {data} from {method.routing_key}")
        print(f"{received_messages} - {received_topics}")

        exceptional = self.check_adaptation_scenario(
            received_messages,
            received_topics,
            self.scenarios["exceptional_scenarios"],
        )
        uncertainty = self.check_adaptation_scenario(
            received_messages,
            received_topics,
            self.scenarios["uncertainty_scenarios"],
        )
        if exceptional:
            if exceptional != "wait":
                print(f"I'm on the scenario {exceptional}")
                received_messages = []
                received_topics = []
                # call effector
            else:
                print("I'll wait to define the exceptional scenario")
        elif self.check_if_is_normal_scenario(
            data, method.routing_key, self.scenarios["normal_scenario"]
        ):
            received_messages = []
            received_topics = []
            print("I'm on normal scenario")
            # call effector to normal
            pass

        elif uncertainty:
            if uncertainty != "wait":
                print(f"I'm on the scenario {uncertainty}")
                received_messages = []
                received_topics = []
                # call effector to uncertainty
            else:
                print("I'll wait to define the uncertainty scenario")
        else:
            received_messages = []
            received_topics = []
            print("All is normal :)")