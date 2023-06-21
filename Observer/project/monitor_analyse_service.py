class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        for scenario in normal_scenario:
            equal_number = 0
            normal_keys = scenario.keys()
            for key in normal_keys:
                if key not in current_scenario.keys():
                    return False
                if current_scenario[key] == scenario[key]:
                    equal_number += 1
            if equal_number == len(normal_keys):
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
                    if self.compare_scenarios(
                        current_scenario[i], adaptation_scenario[scenario][i]
                    ):
                        return "wait"
            if len(current_scenario) >= len(adaptation_scenario[scenario]):
                count = 0
                for i in range(len(current_scenario)):
                    if i >= len(adaptation_scenario[scenario]):
                        break
                    if self.compare_scenarios(
                        current_scenario[i], adaptation_scenario[scenario][i]
                    ):
                        count += 1
                        continue
                    break
                if count == len(adaptation_scenario[scenario]):
                    return scenario

                if len(current_scenario) > len(adaptation_scenario[scenario]):
                    return "uncertainty"

        return False
