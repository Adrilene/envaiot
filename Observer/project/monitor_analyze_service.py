class MonitorAnalyzeService:
    def check_if_is_normal_scenario(self, message, routing_key, normal_scenarios):
        for scenario in normal_scenarios:
            if message["type"] == scenario["type"] and routing_key == scenario["topic"]:
                if scenario["body"] == "*":
                    return True
                elif message["body"] == scenario["body"]:
                    return True
        return False

    def compare_scenarios(self, messages, routing_keys, steps):
        is_same = False
        for i in range(len(messages)):
            if i >= len(steps):
                break

            if (
                steps[i]["topic"] == routing_keys[i]
                and steps[i]["type"] == messages[i]["type"]
            ):
                if steps[i]["body"] == "*":
                    is_same = True
                    continue
                if steps[i]["body"] == messages[i]["body"]:
                    is_same = True
                    continue
                is_same = False
            is_same = False

        return is_same

    def check_adaptation_scenario(self, messages, routing_keys, adaptation_scenarios):
        for scenario_name, steps in adaptation_scenarios.items():
            is_same = self.compare_scenarios(messages, routing_keys, steps)

            if is_same and len(messages) < len(steps):
                return "wait"

            if is_same:
                return scenario_name
