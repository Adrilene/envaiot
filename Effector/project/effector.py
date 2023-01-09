from .plan_execute_service import PlanExecuteService
from .strategies_interpretation import strategies_to_dict


class Effector(PlanExecuteService):
    def __init__(self, strategies):
        self.strategies = strategies_to_dict(strategies)

    def adapt(self, scenario, adapt_type):
        if scenario not in self.strategies.keys():
            return "Scenario not configured."

        return self.plan(self.strategies[scenario][adapt_type])
