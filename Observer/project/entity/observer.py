class Observer:
    def __init__(self, config):
        self.exceptional_scenario = config["exceptional_scenario"]
        self.essential_scenarios = []
        self.scenario_running = ""
        self.normal_scenario = config["normal_scenario"]

    def check_normal_scenario(self, current_scenario):
        check = []
        for i in self.normal_scenario:
            check = []
            for k, v in current_scenario.items():
                if k in i.keys():
                    if v == i[k]:
                        check.append(True)
                    else:
                        check.append(False)
                if len(i) == check.count(True):
                    break
            if check.count(True) == len(i):
                return True
        return False

    def check_essential_exceptional(self):

        check = []
        if not self.essential_scenarios:
            return False

        for i in self.essential_scenarios:
            check.append(self.check_scenario(i))

        if check.count(True) == len(self.exceptional_scenario[self.scenario_running]):
            return True
        return False

    def check_scenario(self, current_scenario):
        is_excp = False
        for key, vl in self.exceptional_scenario.items():
            for i in self.exceptional_scenario[key]:
                check = []
                for k, v in current_scenario.items():
                    if k in i.keys():
                        if i[k] == v:
                            check.append(True)
                        else:
                            check.append(False)
                    if i["body"] != "*":
                        if k in i["body"].keys():
                            if i["body"][k] == v:
                                check.append(True)
                            else:
                                check.append(False)

                if i["body"] != "*":
                    if check.count(True) == len(i):
                        is_excp = True
                        break
                else:
                    if check.count(True) == len(i) - 1:
                        is_excp = True
                        break
            if is_excp:
                self.scenario_running = key
        
        return is_excp

    def is_essential_scenarios(self, current_scenario):
        if self.essential_scenarios == self.exceptional_scenario:
            return False

        return self.check_scenario(current_scenario)

