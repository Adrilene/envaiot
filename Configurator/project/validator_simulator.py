def check_devices_names(devices_names):
	errors = []
	for device in devices_names:
		if (
			not device[0].isupper() and 
			device != device.lower() and 
			device != device.upper() and 
			"_" not in device):
			errors.append(f"{device} is not a valid device name")
	
	return errors


def check_devices_keys(resources):
	errors = []

	for device in resources.keys():
		if ("status" not in resources[device].keys()):
			errors.append(f"Missing status for device {device}")
		if ("senders" not in resources[device].keys()):
			errors.append(f"Missing senders for device {device}")

	return errors


def check_senders(resources):
	errors = []

	for device in resources:
		if device["senders"]:
			for sender in device["senders"]:
				if sender not in resources.keys():
					errors.append(f"Device {sender} does not exist.")

	return errors


def validate_simulator(configuration):
	errors = []
	if ("resources" not in configuration.keys()):
		return "Missing resources key"

	if ("communication" not in configuration.keys()):
		return "Missing communication key"

	errors_for_devices_names = check_devices_names(configuration['resources'].keys())
	errors_for_devices_keys = check_devices_keys(configuration["resources"])
	errors_for_senders = check_senders(configuration["resources"])
	
	if (errors_for_devices_names):
		errors.extend(errors_for_devices_names)

	if (errors_for_devices_keys):
		errors.extend(errors_for_devices_keys)

	if (errors_for_senders):
		errors.extend(errors_for_senders)

	if ("host" not in configuration["communication"].keys()):
		errors.append("Missing host in communication configuration.")

	if ("user" not in configuration["communication"].keys()):
		errors.append("Missing user in communication configuration.")

	if ("password" not in configuration["communication"].keys()):
		errors.append("Missing password in communication configuration.")
	
	return errors
