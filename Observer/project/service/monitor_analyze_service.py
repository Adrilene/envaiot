class MonitorAnalyzeService:
    # def check_running_scenario(self, message, routing_key, scenarios):
    #     running_scenario = ''

    def check_if_is_normal_scenario(self, message, routing_key, normal_scenario):

        if (
            message["type"] == normal_scenario["type"]
            and routing_key == normal_scenario["topic"]
        ):
            if normal_scenario["body"] == "*":
                return True
            elif message["body"] == normal_scenario["body"]:
                return True
        return False

    def check_adaptation_scenario(self, messages, routing_keys, adaptation_scenarios):
        for scenario_name, scenario in adaptation_scenarios.items():
            if len(messages) < len(scenario):
                wait = False
                for i in range(len(messages)):
                    if (
                        messages[i]["type"] == scenario[i]["type"]
                        and routing_keys[i] == scenario[i]["topic"]
                    ):
                        if scenario[i]["body"] == "*":
                            wait = True
                        elif messages[i]["body"] == scenario[i]["body"]:
                            wait = True
                    else:
                        break
                if wait:
                    return "wait"

            if len(messages) == len(scenario):
                is_current = False
                for i in range(len(messages)):
                    if (
                        messages[i]["type"] == scenario[i]["type"]
                        and routing_keys[i] == scenario[i]["topic"]
                    ):
                        if scenario[i]["body"] == "*":
                            is_current = True
                        elif messages[i]["body"] == scenario[i]["body"]:
                            is_current = True
                    else:
                        break

                if is_current:
                    return scenario_name
        return False
