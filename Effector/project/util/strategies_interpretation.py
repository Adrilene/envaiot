def read_action(index, strategies_split):
    action = ""
    if strategies_split[index].upper() == "ON":
        action += strategies_split[index + 1]
        index += 2
        if strategies_split[index].upper() == "STATUS":
            action += f":{strategies_split[index+1]}"
            index += 2
        if ")" in strategies_split[index]:
            return action, index
        else:
            return "Syntax Error!", index


def strategies_to_dict(strategies):
    strategies_dict = {}

    strategies_split = strategies.split(" ")

    index = 0
    key = ""
    while True:
        if index >= len(strategies_split) or strategies_split[index] == ")":
            break
        if strategies_split[index] == "(":
            index += 1
            action, index = read_action(index, strategies_split)
            if action != "Syntax error!":
                strategies_dict[key]["actions"].append(action)
            else:
                return "Syntax Error!"
            index += 1
            continue

        if strategies_split[index].upper() == "IF":
            key = strategies_split[index + 1]
            strategies_dict[key] = {"actions": []}
        index += 2

        if strategies_split[index].upper() == "THEN":
            index += 1
            if strategies_split[index] == "(":
                index += 1
                action, index = read_action(index, strategies_split)
                if action != "Syntax error!":
                    strategies_dict[key]["actions"].append(action)
                else:
                    return "Syntax Error!"
                index += 1
            else:
                return "Syntax Error!"

        else:
            return "Syntax Error!"
    return strategies_dict


actions_dict = strategies_to_dict(
    "IF tv_blocked THEN ( ON SmartTV STATUS available ) IF tv_off THEN ( ON SmartLamp STATUS blink ), ( ON Assistant STATUS play )"
)
print(actions_dict)
