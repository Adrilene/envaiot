class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        print(f"RECEIVED {current_scenario}")
        print(f"REFERENCE {normal_scenario}")
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
        print(f"RECEIVED {current_scenario}")
        print(f"REFERENCE {adaptation_scenario}")
        for scenario in adaptation_scenario:
            if len(current_scenario) < len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if self.compare_scenarios(
                        current_scenario[i], adaptation_scenario[scenario][i]
                    ):
                        return "wait"
                    return False
            if len(current_scenario) >= len(adaptation_scenario[scenario]):
                for i in range(len(current_scenario)):
                    if i >= len(adaptation_scenario[scenario]):
                        break
                    if not self.compare_scenarios(
                        current_scenario[i], adaptation_scenario[scenario][i]
                    ):
                        return False
                if len(current_scenario) > len(adaptation_scenario[scenario]):
                    return "uncertainty"
                return scenario
            return False


# adaptation = {
#     'HighAlcohol': [{'type': 'status', 'body': {'AlcoholLevel': 'high'}, 'topic': 'as_info'}],
#     'HighSpeed': [{'type': 'status', 'body': {'Speed': 'high'}, 'topic': 'ss_info'}]
# }
# sequence = [
#     {'type': 'status', 'body': {'AlcoholLevel': 'high'}, 'topic': 'as_info'}
# ]
# normal = [{"type": "status", "topic": "bm_msg"}]

# print(MonitorAnalyseService().analyse_normal_scenario(sequence[0], normal))
