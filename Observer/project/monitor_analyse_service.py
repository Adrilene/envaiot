class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        if current_scenario == normal_scenario:
            return True

        for curr_scen in current_scenario:
            if curr_scen not in normal_scenario:
                return False
            else:
                return "wait"

        return False

    def compare_scenarios(self, current_scenario, adaptation_scenario):
        if current_scenario == adaptation_scenario:
            return True

        for curr_scen in current_scenario:
            if curr_scen not in adaptation_scenario:
                return False

        if len(current_scenario) > len(adaptation_scenario):
            return "uncertainty"

        return "wait"

    def analyse_adaptation_scenario(self, current_scenario, adaptation_scenario):
        for scenario in adaptation_scenario:
            result = self.compare_scenarios(
                current_scenario, adaptation_scenario[scenario]["scenario"]
            )
            if not result:
                continue

            if result == True:
                return scenario

            return result
