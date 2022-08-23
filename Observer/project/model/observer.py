from ..service.communication_service import CommunicationService
from ..util.connection import subscribe_in_all_queues
from threading import Thread


class Observer(CommunicationService, Thread):
    def __init__(self, communication, scenarios):
        self.normal_scenario = scenarios["normal_scenarios"]
        self.exceptional_scenario = scenarios["exceptional_scenario"]
        self.uncertainty_scenario = scenarios["uncertainty_scenarios"]
        self.queue = "observer"
        self.declare_queue(self.queue)

    def run(self):
        subscribe_in_all_queues(
            communication["host"],
            communication["user"],
            communication["password"],
            communication["exchange"],
            self.queue,
        )
