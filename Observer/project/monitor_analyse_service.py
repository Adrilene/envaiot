class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        if (
            current_scenario["topic"] == normal_scenario["topic"]
            and current_scenario["type"] == normal_scenario["type"]
        ):
            return True
        return False

    def analyse_adaptation_scenario(self, current_scenario, adaptation_scenario):
        """ import ipdb
        ipdb.set_trace() """
        for scenario in adaptation_scenario:
            if len(current_scenario) < len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if 'body' not in adaptation_scenario[scenario][i].keys():
                        current_scenario[i].pop('body')

                    if current_scenario[i] != adaptation_scenario[scenario][i]:
                        return False
                return "wait"

            if len(current_scenario) >= len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if current_scenario[i] != adaptation_scenario[scenario][i]:
                        return False
                if len(current_scenario) > len(adaptation_scenario[scenario]):
                    return "uncertainty"
                return scenario
            return False
