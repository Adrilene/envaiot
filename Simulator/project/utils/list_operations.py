def get_current_device(device_name, devices_list):
    current_device = None
    for device in devices_list:
        if device.name == device_name:
            current_device = device
    return current_device
