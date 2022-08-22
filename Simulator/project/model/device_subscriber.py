import json
from ..service.communication_service import CommunicationService
from ..utils.string_operations import (
    get_queue_name,
    get_subscribing_routing_key,
    get_publishing_routing_key,
)
from threading import Thread


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
        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = body.decode("UTF-8")
        body = json.loads(body)

        print(f"Received {body}")
