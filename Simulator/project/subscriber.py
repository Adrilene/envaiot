import json
import os
from datetime import datetime
from threading import Thread

from dotenv import load_dotenv

from .communication_service import CommunicationService
from .string_operations import (get_publishing_routing_key, get_queue_name,
                                get_subscribing_routing_key)

load_dotenv()
class DeviceSubscriber(CommunicationService, Thread):
    def __init__(self, exchange, device_name, senders):
        CommunicationService.__init__(self, exchange)
        Thread.__init__(self)
        self.device_name = device_name
        queue = get_queue_name(device_name)
        self.declare_queue(queue)
        self.bind_exchange_queue(
            exchange, queue, get_subscribing_routing_key(device_name)
        )

        for sender in senders:
            self.bind_exchange_queue(
                exchange, queue, get_publishing_routing_key(sender)
            )

    def run(self):
        print(f"[*] Starting {self.device_name}")
        self.consume_message(get_queue_name(self.device_name))

    def consume_message(self, queue):
        print(f"[*] {self.device_name} waiting for messages. To exit press CTRL+C")
        self.channel.basic_consume(
            queue=queue,
            on_message_callback=self.callback,
            auto_ack=False,
        )

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        log_file = open(os.getenv("LOGS_PATH"), "a")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)

        log_file.write(
            f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {self.device_name} received {body} from {method.routing_key}"
        )

        log_file.close()
