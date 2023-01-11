class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        if (
            current_scenario["topic"] == normal_scenario["topic"]
            and current_scenario["type"] == normal_scenario["type"]
        ):
            return True
        return False

    def compare_scenarios(self, current_scenario, adaptation_scenario):
        equal_number = 0

        for key in current_scenario.keys():
            if key in adaptation_scenario:
                if current_scenario[key] == adaptation_scenario[key]:
                    equal_number += 1

        if equal_number == len(adaptation_scenario.keys()):
            return True
        return False

    def analyse_adaptation_scenario(self, current_scenario, adaptation_scenario):
        
        for scenario in adaptation_scenario:
            if len(current_scenario) < len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if self.compare_scenarios(current_scenario[i], adaptation_scenario[scenario][i]):
                        return "wait"
                    return False
            if len(current_scenario) >= len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if not self.compare_scenarios(current_scenario[i], adaptation_scenario[scenario][i]):
                        return False
                if len(current_scenario) > len(adaptation_scenario[scenario]):
                    return "uncertainty"
                return scenario
            return False
