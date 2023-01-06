def read_actions(actions):
    actions_list = []
    index = 0

    while True:
        if index >= len(actions):
            break
        
        if actions[index] == "ON":
            actions_list.append(
                f"{actions[index+1]}:{actions[index+3]}"
            )
            index+=4
            continue

        if actions[index] == "OTHERWISE":
            break
    
    return actions_list, index+1

def strategies_to_dict(strategies):
    strategies_list = strategies.split(' ')
    strategies_dict = {}
    key, index = '', 0
    
    while True:
        if index >= len(strategies_list):
            break
        if strategies_list[index] == "IF":
            key = strategies_list[index+1]
            strategies_dict[key] = {
                "adaptive": [],
                "uncertainty": []
            }
            index += 2
            continue
    
        if strategies_list[index] == "THEN":
            strategies_dict[key]["adaptive"], increment = read_actions(strategies_list[index+1:])
            index += increment
            continue

        if strategies_list[index] == "OTHERWISE":
            strategies_dict[key]["uncertainty"], increment = read_actions(strategies_list[index+1:])
            index += increment
            continue
    
        index += 1

    return strategies_dict

""" actions_dict = strategies_to_dict(
    "IF TVBlocked THEN ON SmartTV STATUS available OTHERWISE ON SmartLamp STATUS blink ON Assistant STATUS play"
)
print(actions_dict)
 """