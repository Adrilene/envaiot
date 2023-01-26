import os
import requests
from dotenv import load_dotenv

load_dotenv()


def request_simulator(body):
    return requests.post(f"{os.getenv('SIMULATOR_HOST')}/configure", json=body)


def request_observer(body):
    return requests.post(f"{os.getenv('OBSERVER_HOST')}/configure", json=body)


def request_effector(body):
    return requests.post(f"{os.getenv('EFFECTOR_HOST')}/configure", json=body)
