import requests


def request_simulator(body):
	return requests.post(
		"http://localhost:5001/configure",
		json=body
	)

def request_observer(body):
	return requests.post(
		"http://localhost:5002/configure",
		json=body
	)

def request_effector(body):
	return requests.post(
		"http://localhost:5003/configure",
		json=body
	)

