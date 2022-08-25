class MonitorAnalyzeService:
    def check_if_is_normal_scenario(self, message, routing_key, normal_scenarios):
        for scenario in normal_scenarios:
            if message["type"] == scenario["type"] and routing_key == scenario["topic"]:
                if scenario["body"] == "*":
                    return True
                elif message["body"] == scenario["body"]:
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
                        is_current = False
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
                        is_current = False
                        break

                if is_current:
                    return scenario_name
        return False
