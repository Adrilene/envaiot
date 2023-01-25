import os

from dotenv import load_dotenv

from .plan_execute_service import PlanExecuteService
from .strategies_interpretation import strategies_to_dict

load_dotenv()

class Effector(PlanExecuteService):
    def __init__(self, strategies):
        self.strategies = strategies_to_dict(strategies)

    def adapt(self, scenario, adapt_type):
        log_file = open(os.getenv("LOGS_PATH"), "a")
        if scenario not in self.strategies.keys():
            log_file.write(f"{scenario} is not configured.\n")
            return "Scenario not configured."

        return self.plan(self.strategies[scenario][adapt_type])
