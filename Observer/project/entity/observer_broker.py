import pika
import json
import threading
from pyrabbit.api import Client
from project.util.data import add_new
from .observer import Observer
import requests


class ObserverBroker(threading.Thread, Observer):
    def __init__(self, config):
        threading.Thread.__init__(self)
        Observer.__init__(sconfig)
        self.queue = "observer"
        self.connection_config = config["connection_config"]
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.connection_config["host"])
        )
        self.call_one = True
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue)
        self.subscribe_in_all_queues()

    def get_bindings(self):
        client = Client(
            f'{self.connection_config["host"]}:{self.connection_config["port"]}',
            self.connection_config["user"],
            self.connection_config["password"],
        )

        bindings = client.get_bindings()
        bindings_result = [
            b for b in bindings if b["source"] in self.connection_config["exchanges"]
        ]

        return bindings_result

    def subscribe_in_all_queues(self):
        bindings = self.get_bindings()
        for bind in bindings:
            self.channel.queue_bind(
                exchange=bind["source"],
                queue=self.queue,
                routing_key=bind["routing_key"],
            )

        return bindings

    def callback(self, ch, method, properties, data):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        data = json.loads(data.decode("UTF-8"))
        current_scenario = data
        current_scenario["topic"] = method.routing_key
        print(f"Current Scenario: {current_scenario} - {self.scenario_running}")
        print(f"Exceptional Scenario: {self.exceptional_scenario}")
        is_essential_scenarios = False

        is_essential_scenarios = self.is_essential_scenarios(current_scenario)
        if is_essential_scenarios:
            self.essential_scenarios = add_new(
                self.essential_scenarios, current_scenario
            )

        except_scen = self.check_essential_exceptional()
        print(f"essential Scenario: {list(self.essential_scenarios)} \n\n")
        if except_scen and self.call_one:
            print("==== Cenário excepcional ====")
            requests.get(
                url=f"http://localhost:4002/adapt?scenario={self.scenario_running}"
            )
            self.call_one = False

        # TODO: Como podemos pegar uma lista de cenários normais?
        # Por isso usamos self.normal_messages[0] por enquanto
        if self.check_normal_scenario(current_scenario) and except_scen:
            print("==== Cenário NORMAL ====")
            requests.get(
                url=f"http://localhost:4002/behave_normal?scenario={self.scenario_running}"
            )
            self.essential_scenarios = []
            self.call_one = True
            self.scenario_running = ""
            except_scen = False

    def run(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=False
        )

        self.channel.start_consuming()

    def stop(self):
        raise SystemExit()
