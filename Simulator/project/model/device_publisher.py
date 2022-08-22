import pika

from ..utils.string_operations import get_publishing_routing_key
from ..service.communication_service import CommunicationService


class DevicePublisher(CommunicationService):
    def __init__(self, exchange, device_name):
        CommunicationService.__init__(self, exchange)
        self.routing_key = get_publishing_routing_key(device_name)

    def publish(self, message, device_name):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
            body=json.dumps(message),
        )

        print(f"PUBLISH {device_name} | {message}")
