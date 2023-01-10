def get_sender_routing_key(device_name):
    alias = "".join([c for c in device_name if c.isupper()]).lower()

    return f"{alias}_info"


def get_receiver_routing_key(device_name):
    alias = "".join([c for c in device_name if c.isupper()]).lower()

    return f"{alias}_msg"


def get_exchange_name(project_name):
    return f"{project_name.lower().replace(' ', '_')}_exchange"