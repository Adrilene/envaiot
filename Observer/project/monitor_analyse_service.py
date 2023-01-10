class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        if (
            current_scenario["sender"] == normal_scenario["sender"]
            and current_scenario["type"] == normal_scenario["type"]
        ):
            return True
        return False

    def analyse_adaptation_scenario(self, current_scenario, adaptation_scenario):
        for scenario in adaptation_scenario.keys():
            if len(current_scenario) < len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if current_scenario[i] != adaptation_scenario[scenario][i]:
                        return False
                return "wait"

            if len(current_scenario) == len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if current_scenario[i] != adaptation_scenario[scenario][i]:
                        return False
                return scenario
            return False
